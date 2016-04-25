class Function:
    generalize_attributes = True

    def __init__(self, name, set_name):
        self.name = name
        self.set_name = set_name
        self.attributes = []

    def process_attribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)

        if self.generalize_attributes:
            if "(" in attribute:
                start = attribute.find("(")
                stop = attribute.rfind(")")

                subattribute = attribute[start + 1:stop]

                if "(" in subattribute:
                    # add a more general attribute
                    general_attribute = attribute.replace(subattribute, "p")  # should be more recursive than that...
                    self.process_attribute(general_attribute)
