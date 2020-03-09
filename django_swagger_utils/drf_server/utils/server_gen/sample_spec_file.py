def sample_spec_file(app_name):
    sample_specs_json = """{
      "basePath": "/api/%s/",
      "consumes": [
        "application/json"
      ],
      "produces": [
        "application/json"
      ],
      "security": [
      ],
      "definitions": {
        "User": {
          "description": "This is the description for User model/definition",
          "properties": {
            "firstName": {
              "type": "string"
            },
            "id": {
              "format": "int64",
              "type": "integer"
            },
            "lastName": {
              "type": "string"
            },
            "password": {
              "type": "string"
            },
            "phone": {
              "type": "string"
            },
            "userStatus": {
              "description": "User Status updated",
              "format": "int32",
              "type": "integer"
            },
            "username": {
              "type": "string"
            }
          },
          "type": "object",
          "required": [
            "firstName",
            "lastName",
            "password",
            "phone"
          ]
        },
        "GeneralError" : {
          "type" : "object",
          "properties" : {
            "error_code" : {
              "type" : "integer"
            },
            "error_remarks" : {
              "type" : "string"
            }
          }
        }
      },
      "externalDocs": {
        "description": "Find out more about Swagger",
        "url": "http://127.0.0.1:8000/api"
      },
      "host": "192.168.1.87:8003",
      "info": {
        "contact": {
          "email": "tech@ibtspl.com"
        },
        "description": "This is a sample description",
        "termsOfService": "http://ibtpsl.com",
        "title": "Ib Service",
        "version": "1.0.0"
      },
      "paths": {
        "/user/": {
          "post": {
            "description": "This can only be done by the logged in user. Note: no security implemented yet ",
            "operationId": "createUser",
            "parameters": [
              {
                "$ref": "#/parameters/User"
              }
            ],
            "responses": {
              "200": {
                "description": "user creation success response",
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "username": {
                      "type": "string"
                    }
                  }
                }
              }
            },
            "summary": "Create user",
            "tags": [
              "user"
            ]
          }
        },
        "/user/{username}/": {
          "parameters": [
            {
              "$ref": "#/parameters/UserName"
            }
          ],
          "delete": {
            "description": "This can only be done by the logged in user.",
            "operationId": "deleteUser",
            "responses": {
              "200": {
                "description": "Invalid username supplied",
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "deleted": {
                      "type": "boolean"
                    }
                  }
                }
              },
              "404": {
                "description": "User not found"
              }
            },
            "summary": "Delete user",
            "tags": [
              "user"
            ]
          },
          "get": {
            "parameters": [
              {
                "in": "query",
                "name": "query_param_name",
                "type": "string",
                "description": "Query parameter description"
              }
            ],
            "description": "",
            "operationId": "getUserByName",
            "responses": {
              "200": {
                "description": "user info",
                "schema": {
                  "$ref": "#/definitions/User"
                }
              },
              "404": {
                "description": "User not found"
              },

              "400": {
                "$ref" : "#/responses/GeneralError"
              },
              "401": {
                "description": "User not authenticate"
              }
            },
            "summary": "Get user by user name",
            "tags": [
              "user"
            ]
          },
          "put": {
            "description": "This can only be done by the logged in user.",
            "operationId": "updateUser",
            "parameters": [
              {
                "$ref": "#/parameters/User"
              }
            ],
            "security": [
            ],
            "responses": {
              "400": {
                "description": "Invalid user supplied"
              },
              "404": {
                "description": "User not found"
              },
              "200": {
                "description": "Update users",
                "schema": {
                  "$ref": "#/definitions/User"
                }
              }
            },
            "summary": "Updated user",
            "tags": [
              "user"
            ]
          }
        }
      },
      "schemes": [
        "http"
      ],
      "securityDefinitions": {
        "oauth": {
          "tokenUrl": "http://auth.ibtspl.com/oauth2/",
          "flow": "password",
          "scopes": {
            "read": "read users",
            "write": "create users",
            "update": "update users",
            "delete": "delete users"
          },
          "type": "oauth2"
        }
      },
      "swagger": "2.0",
      "tags": [
        {
          "description": "Operations about user",
          "externalDocs": {
            "description": "Find out more about our store",
            "url": "http://swagger.io"
          },
          "name": "user"
        }
      ],
      "parameters": {
        "User": {
          "description": "User Parameter",
          "in": "body",
          "name": "user",
          "required": true,
          "schema": {
            "$ref": "#/definitions/User"
          }
        },
        "UserName": {
          "description": "username of the user description",
          "in": "path",
          "name": "username",
          "required": true,
          "type": "string"
        }
      },
      "responses": {
        "GeneralError": {
          "description": "General Error",
          "schema": {
            "$ref": "#/definitions/GeneralError"
          }
        }
      }
    }
    """ % app_name
    return sample_specs_json
