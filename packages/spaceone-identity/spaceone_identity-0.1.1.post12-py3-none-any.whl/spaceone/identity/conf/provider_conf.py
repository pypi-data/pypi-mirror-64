DEFAULT_PROVIDERS = [{
    'provider': 'aws',
    'name': 'AWS',
    'template': {
        'data': [{
            'key': 'account_id',
            'name': 'Account ID',
            'type': 'str',
            'is_required': True
        }]
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
        'data': [{
            'key': 'sa_name',
            'name': 'Service Account Name',
            'type': 'str',
            'is_required': True
        }, {
            'key': 'project_id',
            'name': 'Project ID',
            'type': 'str',
            'is_required': True
        }]
    },
    'capability': {
        'supported_schema': ['google_application_credentials']
    },
    'tags': {
        'icon': 'https://assets-console-cloudone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/gcp-cloudservice.png'
    }
}]
