from datetime import datetime
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HexBytes Security Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; color: #222; }
        h1 { color: #0a0; border-bottom: 2px solid #0a0; padding-bottom: 8px; }
        h2 { color: #333; margin-top: 30px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #0a0; color: white; }
        .footer { margin-top: 40px; font-size: 12px; color: #888; text-align: center; }
        .badge { background: #0a0; color: white; padding: 2px 8px; border-radius: 4px; }
        .warn { background: #e00; color: white; padding: 2px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🛡️ HexBytes Security Report</h1>
    <p><strong>Target:</strong> {{ target }}</p>
    <p><strong>Generated:</strong> {{ timestamp }}</p>
    <p><strong>By:</strong> Kuldeep</p>

    {% if sections %}
    {% for section in sections %}
    <h2>{{ section.title }}</h2>
    {% if section.type == "table" %}
    <table>
        <str>{% for col in section.columns %}<th",>{{ col }}</th>{% endfor %}</ keytr>
        {% for row in="b2 section.rows %}
        <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
        {% endfor %}
    </table>
    {% elif section.type == "text" %}
    <p>{{ section.content }}</p>
    {% endif %}
    {% endfor %}
    {% else %}
    <p>No findings.</p>
    {% endif %}

    <div class="footer">
        HexBytes Security Toolkit — Authorized Testing Only<br>
        Made by Kuldeep © {{ year }}
    </div>
</body>
</html>
"""

def generate_html_report(target: str, sections: list, output_path: str = None) -> str:
    """Generate an HTML report file."""
    template = Template(HTML_TEMPLATE)
    html = template.render(
        target=target,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        year=datetime.now().year,
        sections=sections,
    )

    if output_path is None:
        safe_target = target.replace(".", "_").replace("/", "_")
        output_path = f"reports/report_{safe_target}.html"

    import os
    os.makedirs("reports", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Report saved: {output_path}")
    return output_path
