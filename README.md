# getSinceraData

Basically how this is going to work is via a GitHub Action. On every merge to the `master` branch it will hit up the Sincera API, retrieve the ecosystem data, store it as an artifact and probably format it and put it on S3. Maybe later we'll add some visualization of that object
