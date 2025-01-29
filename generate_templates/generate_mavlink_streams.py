#!/usr/bin/python3
import os
import sys

class name_variations:
    def __init__(self,msg_name):
        self.snake_case=msg_name.split(".")[0]
        self.caps_case = self.snake_case.upper()
        self.camel_case=self.to_camel_case(self.snake_case)



    def to_camel_case(self, snake_case):
        tmp_str=""
        upper_first_words = [x[0].upper() +x[1:] for x in snake_case.split("_")]
        for word in upper_first_words:
            tmp_str+=word
        return tmp_str

class create_streams(name_variations):
    def __init__(self, path, template_file):
        self.path=os.path.realpath(os.path.expanduser(path))
        super().__init__(os.path.basename(self.path))
        self.fin = template_file
        self.header_line_lst=[]
        self.header_file=self.caps_case+".hpp"
        self.xml_line_lst=[]


    def add_msg_fields_to_header_file(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.replace('\t', " ")
                line = line.strip()
                if not line == "" and not "=" in line:
                    field_type, field_name = line.split(" ")[0].strip(), line.split(" ")[1].strip()
                    self.header_line_lst.append(f"\t\t\t_msg_{self.snake_case}.{field_name} = _{self.snake_case}.{field_name};\n")




    def generate_header_file(self):
        print(f"[INFO] generating {self.caps_case}.msg header file")
        camel_case_replace="@CamerlCase@"
        snake_case_replace="@SnakeCase@"
        caps_case_replace="@ALLCAPS@"
        with open(self.fin, "r") as fin:
            for line in fin:
                if "@MESSAGE_INSERT_HERE@" in line:
                    self.add_msg_fields_to_header_file()
                else:
                    line=line.replace(camel_case_replace,self.camel_case)
                    line=line.replace(snake_case_replace,self.snake_case)
                    line=line.replace(caps_case_replace,self.caps_case)
                    self.header_line_lst.append(line)
        with open(f"{self.caps_case}.hpp","w") as fout:
            for line in self.header_line_lst:
                fout.write(line)
        print(f"[INFO] move {self.header_file} to {'/'.join(self.path.split('/')[:-2])}/src/modules/mavlink/streams")
        print(f"[INFO] need to modify StreamsList in {'/'.join(self.path.split('/')[:-2])}/src/modules/mavlink/mavlink_messages.cpp")


    def generate_xml(self):
        print(f"[INFO] generating {self.snake_case}.msg xml message definition to add to rb5000.xml")
        print("========================================================================")
        self.xml_line_lst.append(f"<message id=\"<replace with num between 180-229>\" name=\"{self.caps_case}\">")
        self.xml_line_lst.append(f"\t<description>Publish {self.caps_case}</description>")



        with open(self.path, "r") as f:
            for line in f:
                line = line.replace('\t', " ")
                line = line.strip()
                if not line == "" and not "=" in line:
                    field_type, field_name = line.split(" ")[0].strip(), line.split(" ")[1].strip()
                    if "float" in field_type:
                        field_type=field_type.replace("float32","float")
                        field_type=field_type.replace("float64","float")
                    elif "int" in field_type:
                        tmp = field_type.split("[")
                        tmp[0]= tmp[0]+"_t"
                        field_type="".join(tmp)

                    self.xml_line_lst.append(f"\t<field type=\"{field_type}\" name=\"{field_name}\"> {self.snake_case} {field_name} reading </field>")
        self.xml_line_lst.append("</message>")
        for line in self.xml_line_lst:
            print(line)







if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[ERROR]")
        exit(1)

    path = os.path.realpath(os.path.expanduser(sys.argv[1]))

    if path.split("/")[-3] != "PX4-Autopilot" or path.split(".")[-1] != "msg":
        print("incorrect path expected <path-to-PX4-Autopilot>/msg/<custom_msg>.msg")
        exit(1)


    x = create_streams(path,"streams_template.txt")
    x.generate_header_file()
    print("========================================================================")
    x.generate_xml()


