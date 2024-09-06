import openai
from pathlib import Path
from tqdm import tqdm
def check(folder_path,outpath):
    # 遍历文件夹下的所有文件
    folder_path=Path(folder_path)
    file_paths = sorted([file for file in folder_path.iterdir() if file.is_file()])
    for file_path in tqdm(file_paths, desc="Reading files"):
        # 检查是否为文件（忽略子文件夹）
        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                with open(outpath,"a+",encoding="utf-8") as f:
                    f.write(f'{file_path.name} ')
                    f.write(checkout(content)+'\n')
                
def checkout(contents):
    openai.api_key = "sk-XGe4YHG1wo3V5sCfB24bD1A9Df944d54B1407247F30b8aDc"
    openai.base_url = "https://api.v3.cm/v1/"
    openai.default_headers = {"x-foo": "true"}

    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"""{contents}""",
            },
            {
                "role":"system",
                "content":f"""You are a helpful assistant in code audit. First, you should tell me Whether the code has vulnerabilities, if so tell me what kind of vulnerability it belongs to. Second, give me some advice to fix it.You should output in the format like: ' Trojan horse or Online banking Trojans or Safe.\n Fix: ' Don't output any other information please!""",
            }
        ],
    )
    answer=completion.choices[0].message.content
    return (answer)


if __name__=="__main__":
    check(folder_path = './folder/test',outpath="./result.txtz")
    #检测folder_path路径下的所有代码文件,将检测结果输出到outpath路径文件中
