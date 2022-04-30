import os
import sys

input = "~/robotics/QCOM_UBUN/PX4-Autopilot/msg/sensor_baro.msg"
path = os.path.realpath(os.path.expanduser(input))

msg_name=os.path.basename(path)

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
        self.line_lst=[]


    def get_fields(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.replace('\t', " ")
                line = line.strip()
                if not line == "" and not "=" in line:
                    field_type, field_name = line.split(" ")[0].strip(), line.split(" ")[1].strip()
                    self.line_lst.append(f"\t\t\t_msg_{self.snake_case}.{field_name} = _{self.snake_case}.{field_name};")


    def generate_line_lst(self):
        camel_case_replace="@CamerlCase@"
        snake_case_replace="@SnakeCase@"
        caps_case_replace="@ALLCAPS@"
        with open(self.fin, "r") as fin:
            for line in fin:
                if "@MESSAGE_INSERT_HERE@" in line:
                    self.get_fields()
                else:
                    line=line.replace(camel_case_replace,self.camel_case)
                    line=line.replace(snake_case_replace,self.snake_case)
                    line=line.replace(caps_case_replace,self.caps_case)
                    self.line_lst.append(line)
        with open("tmp.txt","w") as fout:
            for line in self.line_lst:
                fout.write(line)








x = create_streams(input,"streams_template.txt")
x.generate_line_lst()


if msg_name.split(".")[-1] != "msg":
    print("not a .msg please provide a custom .msg from PX4-Autopilot/msg/<custom_msg>.msg")

if not os.path.exists(path):
    print("this .msg doesnt exist")


def get_fields(path):
    fields = []
    with open(path,"r") as f:
        for line in f:
            line=line.replace('\t'," ")
            line=line.strip()
            if not line=="" and not "=" in line:
                field_type, field_name = line.split(" ")[0].strip(), line.split(" ")[1].strip()
                fields.append([field_type,field_name])
    for x in fields:
        print(x)
