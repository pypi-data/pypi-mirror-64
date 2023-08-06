# httpie-apikey-auth

[Elastic ApiKey](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html) auth plugin for [HTTPie](https://github.com/jkbr/httpie>).

## Installation

```bash
pip install httpie-apikey-auth
```

You should now see `apikey` under `--auth-type` in `$ http --help` output.

## Usage

```bash
http --auth-type=apikey --auth='id:api_key' es.example.org:9200
```


