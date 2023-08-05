[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new)

# pulumi-google-analytics

This project contains a pip packaged named `pulumi-google-analytics` which allows Google Analytics resources to be managed in Pulumi.

An example Pulumi program which uses this package is present in the `example` folder.

## Setup

* Install the package into your Pulumi project using `pip`

```
$ pip install pulumi-google-analytics
```

* Set your Google credentials in your stack config:

```
$ pulumi config set aws:region <region>
$ pulumi config set google_api_key_file <google-api-key-file>
$ pulumi config set ga_account_id <google-analytics-manager-account-id>
```


## Directory structure

```
.
├── example
│   ├── __main__.py
│   ├── Pulumi.yaml
│   └── README.md
├── pulumi_google_tag_manager
│   └── dynamic_providers
│       ├── web_property_provider.py
│       ├── web_property.py
│       └── service.py
├── README.md
├── requirements.txt
└── setup.py
```
