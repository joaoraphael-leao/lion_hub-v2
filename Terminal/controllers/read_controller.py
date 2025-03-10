class SeeClasses:
    def get(self, database, class_name):
        if not database:
            print(f"Nenhum {class_name} disponível")
            return
        for item in database:
            print(item)

