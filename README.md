# translatte
For translating your JSON between languages, applies the Google Translate API to every string value, recursively through the entire file -has no effect on keys

Requirements:
- gCloud CLI needs to be [initialized](https://cloud.google.com/sdk/docs/initializing).
- [Translation API](https://cloud.google.com/translate) needs to be enabled.
- settings.toml copy and alter it:
    `cp settings.toml.example settings.toml`  

You do not need to set the Google Cloud Platform project id, [script will default to the one set at initialization](https://cloud.google.com/sdk/docs/initializing).

Used on [Reactive-Resume](https://github.com/AmruthPillai/Reactive-Resume) to translate from English to Icelandic:  
``` 
    from_path = "./Reactive-Resume/client/public/locales/en"
    to_path = "./Reactive-Resume/client/public/locales/is"
    from_lang = 'en-US'
    to_lang = 'is-IS'
```