class HttpRequest:
    def __init__(
        self,
        header = None,
        body = None,
        query_params = None,
        path_params = None,
        url = None,
        ipv4 = None,
        form_data = None
    ) -> None:
        self.header = header
        self.body = body
        self.query_params = query_params
        self.path_params = path_params
        self.url = url
        self.ipv4 = ipv4
        self.form_data = form_data

    def get_access_token(self) -> str:
        """
        Extract access token from Authorization header.
        Handles both 'Bearer <token>' and plain token formats.
        
        Returns:
            str: The access token without Bearer prefix
        """
        authorization = self.header.get("authorization", "")

        if authorization.lower().startswith("bearer "):
            return authorization[7:].strip()

        return authorization.strip()
