from flask_sqlalchemy.model import Model
import app.models as module_models

TABLES = [
    element
    for x in dir(module_models) 
    if 
        isinstance((element := getattr(module_models, x)), type) 
        and issubclass(element, Model)
]

def generate_dataview():

    data = {} 
    for table in TABLES: 
        columns = [c.name for c in table.__table__.columns] 
        data[table.__name__] = [ 
            {
                column: getattr(v, column) 
                for column in columns
            } for v in table.query.all() 
        ]

    tables_html = ''
    for table_name, rows in data.items():
        if not rows:
            continue
        
        columns = rows[0].keys() 
        tables_html += f"<h2>{table_name}</h2><table><thead><tr>" 
        for column in columns: 
            tables_html += f"<th>{column}</th>" 
        tables_html += "</tr></thead><tbody>" 
        for row in rows: 
            tables_html += "<tr>" 
            for column in columns: 
                tables_html += f"<td>{row[column]}</td>" 
            tables_html += "</tr>" 
        tables_html += "</tbody></table>"

    return f"""
    <!DOCTYPE html> 
    <html lang="en"> 
    <head> 
        <meta charset="UTF-8"> 
        <title>DataView</title> 
        <style> 
            body {{ 
                font-family: Arial, sans-serif; 
                background-color: #121212; 
                color: #e0e0e0; 
                margin: 0; 
                padding: 20px; 
            }} 
            h1, h2 {{ 
                color: #bb86fc; 
            }} 
            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin: 20px 0; 
                background-color: #1e1e1e; 
            }} 
            table, th, td {{ 
                border: 1px solid #444; 
            }} 
            th, td {{ 
                padding: 12px; 
                text-align: left; 
            }} 
            th {{ 
                background-color: #2c2c2c; 
                color: #bb86fc; 
            }} 
            tr:nth-child(even) {{ 
                background-color: #1e1e1e; 
            }} 
            tr:nth-child(odd) {{ 
                background-color: #2c2c2c; 
            }} 
            a {{ 
                color: #bb86fc; 
                text-decoration: none; 
            }} 
            a:hover {{ 
                text-decoration: underline; 
            }} 
        </style>
    </head>
    <body> 
        <h1>[admin]: DataView</h1>
        {tables_html}
    </body>
    """
