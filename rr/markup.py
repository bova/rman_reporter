from jinja2 import Environment, FileSystemLoader


class HTML:
    def __init__(self):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        self.template = env.get_template('report.html')

    def render(self, backup_summary_list, backup_detail_dict):
        return self.template.render(backup_summary_list=backup_summary_list, backup_detail_dict=backup_detail_dict)


if __name__ == '__main__':
    html = HTML()
