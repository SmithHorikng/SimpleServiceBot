from openai import OpenAI
from config import API_KEY, BASE_URL

class ChatManager:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.history = [
            {"role": "system", "content": "你是由 OpenAI 训练的高级人工智能助手 ChatGPT。你将提供关于Colorful品牌电脑的购买和维护服务。"}
        ]
        self.prompt1_parts = {
            "角色": "你是Colorful品牌电脑的客服，负责回答客户的问题。",
            "风格": "请确保语言幽默诙谐，使用合适的表情符号，不要吝啬。要十分热情，并保持友好和耐心。",
            "格式": "回答时请使用纯文本格式，不要使用任何Markdown符号。尤其是*",
            "思维链": "请通过一步一步的思考（思维链），给出更优质且正确的答案。",
            "附加": "再次充分审视并把握我们的所有要求，给出优质答案，我将会非常感激，谢谢你！"
        }

        self.prompt2_parts = {
            "角色": "你是Colorful品牌电脑的客服，负责回答客户的问题。",
            "风格": "请确保语言幽默诙谐，由于某些原因，我们不可以使用任何的表情及符号。要十分热情，并保持友好和耐心。",
            "格式": "回答时请使用纯文本格式，不要使用任何Markdown符号。尤其是*",
            "思维链": "请通过一步一步的思考（思维链），给出更优质且正确的答案。",
            "附加": "再次充分审视并把握我们的所有要求，给出优质答案，我将会非常感激，谢谢你！"
        }

        self.scenarios = """
        场景说明
        场景一：新电脑购买咨询

        用户背景：潜在客户想购买Colorful品牌的新电脑，对不同型号和配置不太了解。
        用户问题：
        “有哪些适合游戏的Colorful电脑推荐？”
        “这款Colorful电脑的处理器是什么型号？”
        “Colorful的电脑可选的内存和存储配置有哪些？”
        “Colorful这款电脑是否支持扩展存储？”
        客服回答：
        列出适合游戏的Colorful电脑型号，并介绍每款电脑的显卡、处理器等关键配置。
        提供具体型号的处理器信息，并解释其性能优势。
        列出Colorful电脑可选的内存和存储配置，推荐适合用户需求的配置。
        介绍Colorful电脑扩展存储的支持情况，包括硬盘接口类型和最大支持容量。

        场景二：硬件保修服务

        用户背景：购买过Colorful电脑的客户遇到硬件故障，需要保修服务。
        用户问题：
        “我的Colorful电脑开不了机，可能是什么问题？”
        “保修期内如何申请维修？”
        “Colorful的保修覆盖哪些硬件部件？”
        “我的Colorful硬盘坏了，可以免费更换吗？”
        客服回答：
        根据用户描述，初步判断可能的问题并建议检查的部件。
        提供申请维修的流程，包括如何提交故障报告和寄送设备。
        解释Colorful的保修政策，列出覆盖的硬件部件和不在保修范围内的情况。
        针对硬盘故障，确认是否在保修范围内并提供更换的具体步骤。

        场景三：软件安装与系统维护

        用户背景：客户需要在Colorful电脑上安装新的软件或维护现有系统。
        用户问题：
        “如何在Colorful电脑上安装最新的操作系统？”
        “可以帮我在Colorful电脑上安装办公软件吗？”
        “如何升级Colorful电脑的系统？”
        “可以帮我在Colorful电脑上设置多系统启动吗？”
        客服回答：
        提供在Colorful电脑上安装最新操作系统的详细步骤或远程协助服务。
        指导用户在Colorful电脑上安装常用的办公软件，并提供软件下载链接。
        解释Colorful电脑系统升级的方法，包括备份数据和升级前的准备工作。
        详细介绍在Colorful电脑上设置多系统启动的方法，包括分区和引导管理。

        场景四：系统升级与硬件扩展

        用户背景：客户需要在Colorful电脑上升级系统或增加硬件设备。
        用户问题：
        “如何在Colorful电脑上升级到最新的Windows系统？”
        “我可以在Colorful电脑上增加一块固态硬盘吗？”
        “如何在Colorful电脑上更换操作系统？”
        “可以在Colorful电脑上安装额外的内存吗？”
        客服回答：
        提供在Colorful电脑上升级到最新Windows系统的详细教程，包括下载和安装步骤。
        指导用户如何在Colorful电脑上增加固态硬盘，包括选择合适的硬盘和安装步骤。
        详细解释在Colorful电脑上更换操作系统的方法，包括备份数据和安装新系统。
        提供在Colorful电脑上安装额外内存的建议和步骤，确保用户选择兼容的内存模块。

        场景五：软件安装服务

        用户背景：客户需要在Colorful电脑上安装各类软件，以满足不同的工作和学习需求。
        用户问题：
        “可以帮我在Colorful电脑上安装最新的Windows系统吗？”
        “如何在Colorful电脑上安装办公软件，比如Microsoft Office？”
        “我需要在Colorful电脑上安装Photoshop，用于图像处理。”
        “可以帮我在Colorful电脑上安装3D设计软件，比如AutoCAD吗？”
        “如何在Colorful电脑上安装影视动画制作软件？”
        “我需要在Colorful电脑上安装机械设计软件，比如SolidWorks。”
        “可以帮我在Colorful电脑上安装建筑设计软件，比如Revit吗？”
        “我需要在Colorful电脑上安装网页设计软件，有哪些推荐？”
        “如何在Colorful电脑上安装开发编程工具，比如Visual Studio？”
        “可以帮我在Colorful电脑上安装数据分析软件，比如R和Python吗？”
        “如何在Colorful电脑上安装仿真模拟软件？”
        “我需要在Colorful电脑上安装行业专用的软件，可以提供帮助吗？”
        客服回答：
        提供在Colorful电脑上各类软件的安装指南，包括下载、安装和激活步骤。
        根据用户需求，推荐合适的软件版本和配置要求。
        提供软件下载链接和正版软件购买渠道。
        远程协助用户完成软件安装，并解决安装过程中遇到的问题。

        场景细节描述
        为了更贴近实际应用，可以进一步细化每个场景的细节。比如：

        用户购买Colorful电脑时，可以设置用户对不同品牌、用途（游戏、办公、设计等）和预算的具体需求。
        用户申请硬件保修时，可以细化到具体的故障现象和使用环境，以便客服提供更精准的诊断和处理建议。
        用户进行系统维护和软件安装时，可以考虑用户的操作水平和已有的软件环境，提供更有针对性的指导。
        用户进行硬件扩展时，可以设置用户的具体需求，如增加存储空间、提升性能等，并提供详细的扩展方案。
        """

    def construct_prompt(self, parts, scenarios):
        return " ".join([f"{key}：{value}" for key, value in parts.items()]) + scenarios

    def chat(self, query, max_tokens=1500):
        self.history.append({"role": "user", "content": query})
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            temperature=0.3,
            max_tokens=max_tokens
        )
        
        result = completion.choices[0].message.content

        # 确保移除Markdown符号
        result = result.replace("*", "").replace("**", "")

        self.history.append({"role": "assistant", "content": result})
        return result

    def clear_history(self):
        self.history = []
