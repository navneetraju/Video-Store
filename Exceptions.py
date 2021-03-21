class Neo4JFailedRequest(Exception):
    """Exception raised for failed requests
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Neo4JWrongDB(Exception):
    """Exception raised for invalid database names
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)