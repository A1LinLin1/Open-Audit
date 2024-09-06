import datetime
import json
import os
import subprocess
from collections import Counter

from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import legal, landscape
from reportlab.lib.colors import HexColor
import stateManager


morandi_colors = [
    HexColor("#005a45"),
    HexColor("#ffe393"),
    HexColor("#bbc375"),
    HexColor("#7ba064"),
    HexColor("#407e54"),
    HexColor("#407e54"),
    HexColor("#FF99CC"),
    HexColor("#CC99CC"), #7
    HexColor("#363636"), #8
    HexColor("#cbcbff"),#9
    HexColor("#bdbdbd"), #10
    HexColor("#f6f6f6"),#11
    HexColor("#383c41"),#12 标题背景
    HexColor("#24693b"), #13 表格表头
    HexColor("#b1d3c5"), #14 表格表头候选（浅）
    HexColor("#EFFFF1"), #15 表格内部
    HexColor("#E9FFF2") # 16 表格内部2

]
title_font_name = "NotoSansSC-Bold"
title_font_path = "Noto_Sans_SC/static/NotoSansSC-Bold.ttf"
body_font_name = "NotoSansSC-Regular"
body_font_path = "Noto_Sans_SC/static/NotoSansSC-Regular.ttf"


pdfmetrics.registerFont(TTFont(title_font_name, title_font_path))
pdfmetrics.registerFont(TTFont(body_font_name, body_font_path))


# 定义一个新的页面大小
custom_page_size = (landscape(legal)[0], 1.7 * landscape(legal)[1])

def generate_pie_chart_with_legend(data, labels):
    d = Drawing(1000, 350)
    pie = Pie()
    pie.x = 200
    pie.y = 20
    pie.width = 300
    pie.height = 300
    pie.data = data
    total = sum(data)
    pie.labels = [f"{int((item / total) * 100)}%" for item in data] # 计算百分比
    pie.sideLabels = True # 使用侧面标签
    pie.slices.strokeWidth = 0.5 # 加粗扇区之间的线条宽度
    pie.slices.strokeColor = HexColor("#E5E5E5") # 设置扇区之间的线条颜色
    for i, color in enumerate(morandi_colors[:len(data)]): # 设置扇区的颜色
        pie.slices[i].fillColor = color
    d.add(pie)

    legend_x = 540
    legend_y = 160
    legend_height = 20
    legend_gap = 5

    for i, label in enumerate(labels):
        d.add(Rect(legend_x, legend_y - i * (legend_height + legend_gap), legend_height, legend_height, fillColor=pie.slices[i].fillColor))
        d.add(String(legend_x + legend_height + 5, legend_y - i * (legend_height + legend_gap) + 5,
            f"{label}丨个数：{data[i]}", fontName=body_font_name, fontSize=15))

    return d


def generate_pdf_report(results, last_folder):
    with open(results, 'r', encoding='utf-8') as file:
        results = json.load(file)
    report_name = last_folder + "漏洞扫描报告"
    report_name += datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Create a new PDF document
    # doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))
    output_path = "report\\" + report_name + '.pdf'
    doc = SimpleDocTemplate(output_path, pagesize=custom_page_size, bottomMargin=36)
    elements = []

    # 获取样式
    styles = getSampleStyleSheet()

    # 设置标题样式
    styles['Heading1'].fontName = title_font_name
    styles['Heading1'].fontSize = 35
    styles['Heading1'].leading = 24
    styles['Heading1'].alignment = 1  # 1 代表居中
    styles['Heading1'].textColor = colors.white

    # 设置正文样式
    styles['Normal'].fontName = body_font_name
    styles['Normal'].fontSize = 14
    styles['Normal'].leading = 14.4

    vulnerability_descriptions = [item["漏洞描述"] for item in results]
    description_counts = Counter(vulnerability_descriptions)

    # 标题
    title = Paragraph("Open-Audit——" + report_name, styles['Heading1'])
    # 将标题放入一个单元格的表格中
    title_table = Table([[title]], colWidths=[1500], rowHeights=100)
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), morandi_colors[12]),  # 设置背景颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 文字居中
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # 下边距
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # 左边距
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # 右边距
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # 外边框
    ]))
    elements.append(title_table)
    elements.append(Spacer(1, 40))  # 20单位的垂直空白
    # elements.append(title)
    # elements.append(Spacer(1, 40))  # 20单位的垂直空白

    # 饼状图和图例
    pie_chart = generate_pie_chart_with_legend(list(description_counts.values()), list(description_counts.keys()))
    elements.append(pie_chart)

    elements.append(Spacer(1, 40))  # 20单位的垂直空白


    # 总结
    summary_text = f'审计结果：发现可疑漏洞总数: <font color="red"><strong>{len(results)}</strong></font> 个'
    summary = Paragraph(summary_text, styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 30))  # 20单位的垂直空白


    # 定义表头
    table_data = [['ID', '漏洞描述', '文件路径', '漏洞详细']]


    # 表格数据植入
    for idx, result in enumerate(results, 1):
        table_data.append([
            idx,
            Paragraph(result['漏洞描述'], styles['Normal']),
            Paragraph(result['文件路径'], styles['Normal']),
            Paragraph(result['漏洞详细'], styles['Normal'])
        ])
    # 创建表格
    table = Table(table_data, colWidths=[50, 350, 200, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), morandi_colors[13]),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 设置垂直居中对齐
        ('FONTNAME', (0, 0), (-1, -1), body_font_name),  # 设置整个表格的字体为正文字体
        ('FONTNAME', (0, 0), (-1, 0), title_font_name),  # 设置表头的字体为标题字体
        ('FONTSIZE', (0, 0), (-1, 0), 16),  # 设置表头字体大小
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), morandi_colors[15]),
        ('GRID', (0, 0), (-1, -1), 1, morandi_colors[7]),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # 设置单元格自动换行（支持中日韩字符）
        ('LEADING', (0, 0), (-1, -1), 14)
    ]))



    elements.append(table)
    # 生成PDF
    doc.build(elements)
    # 创建 'report' 文件夹（如果不存在）
    report_folder = 'report'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # output_path = os.path.join(report_folder, report_name + ".pdf")
    # generate_pdf_report(results)
    try:
        print(output_path)
        subprocess.Popen([output_path], shell=True)
    except Exception as e:
        print("打开PDF文件失败：", str(e))



# if __name__ == "__main__":
#     # 测试代码
#     with open('results.json', 'r', encoding='utf-8') as file:
#         results = json.load(file)
#
#
#     report_name = "漏洞报告"
#     report_name += datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     print(report_name)
#
#     generate_pdf_report(results, report_name+".pdf", report_name)
#     print("success！")
