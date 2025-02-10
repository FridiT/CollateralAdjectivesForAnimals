from pathlib import Path

template = """
<head>
    <title>Collateral Adjectives</title>
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid black;
            padding: 10px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h2>Collateral Adjective Table</h2>
    <table>
        <tr>
            <th>Collateral Adjectives</th>
            <th>Animal</th>
            <th>Picture</th>
        </tr>
        {rows}
    </table>
</body>
</html>
"""


class GenerateHTML:

    @staticmethod
    def generate_html(data):
        """
        Description: the function get the data and generate HTML file that contain table with all the data
        :param data: dictionary with collateral adjective with the animals that belong him
        """
        rows = ""
        for collateral_adjective, obj in data.items():
            # define flag for the collateral adjective column - to order the animals in the relevant collateral adjective row
            first_row = True
            for animal in obj.animals:
                image = f'<img src="{animal.local_image_link}" alt="">' if animal.local_image_link else ''

                rows += f"""
                <tr>
                    {'<td rowspan="' + str(len(obj.animals)) + '">' + collateral_adjective + '</td>' if first_row else ''}
                    <td>{animal.name}</td>
                    <td>{image}</td>
                </tr>
                """
                first_row = False
        # set the rows into the page template
        html_content = template.format(rows=rows)

        # Save the html file
        output_file = Path("Collateral Adjectives For Animals.html")
        output_file.write_text(html_content)
