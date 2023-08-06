DEFAULT_PROVIDERS = [{
    'provider': 'aws',
    'name': 'AWS',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'account_id': {
                        'title': 'Account ID',
                        'type': 'string'
                    }
                },
                'required': ['account_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['aws_access_key', 'aws_assume_role']
    },
    'tags': {
        'icon': 'https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg'
    }
}, {
    'provider': 'gcp',
    'name': 'Google Cloud Platform',
    'template': {
        'service_account': {
            'schema': {
                'type': 'object',
                'properties': {
                    'sa_name': {
                        'title': 'Service Account',
                        'type': 'string'
                    },
                    'project_id': {
                        'title': 'Project ID',
                        'type': 'string'
                    }
                },
                'required': ['sa_name', 'project_id']
            }
        }
    },
    'capability': {
        'supported_schema': ['google_application_credentials']
    },
    'tags': {
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/gcp-cloudservice.png'
    }
}]
