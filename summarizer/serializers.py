from rest_framework import serializers

class SummarizationSerializer(serializers.Serializer):
    INPUT_TYPES = [('text', 'Text'), ('file', 'File'), ('url', 'URL')]
    FORM_TYPES = [('text', 'Text'), ('bullet', 'Bullet Points')]
    LANGUAGES = [
        ('English', 'English'),
        ('French', 'French'),
        ('German', 'German'),
        ('Polish', 'Polish'),
        ('Spanish', 'Spanish'),
        ('Ukrainian', 'Ukrainian'),
        ('Arabic', 'Arabic'),
        ('Bengali', 'Bengali'),
        ('Bulgarian', 'Bulgarian'),
        ('Chinese simplified and traditional', 'Chinese simplified and traditional'),
        ('Czech', 'Czech'),
        ('Croatian', 'Croatian'),
        ('Dutch', 'Dutch'),
        ('Danish', 'Danish'),
        ('System', 'System'),
        ('Estonian', 'Estonian'),
        ('Finnish', 'Finnish'),
        ('Greek', 'Greek'),
        ('Hebrew', 'Hebrew'),
        ('Hindi', 'Hindi'),
        ('Hungarian', 'Hungarian'),
        ('Indonesian', 'Indonesian'),
        ('Italian', 'Italian'),
        ('Japanese', 'Japanese'),
        ('Korean', 'Korean'),
        ('Latvian', 'Latvian'),
        ('Lithuanian', 'Lithuanian'),
        ('Norwegian', 'Norwegian'),
        ('Portuguese', 'Portuguese'),
        ('Romanian', 'Romanian'),
        ('Russian', 'Russian'),
        ('Serbian', 'Serbian'),
        ('Slovak', 'Slovak'),
        ('Slovenian', 'Slovenian'),
        ('Swahili', 'Swahili'),
        ('Swedish', 'Swedish'),
        ('Turkish', 'Turkish'),
        ('Thai', 'Thai'),
        ('Vietnamese', 'Vietnamese'),
    ]
    GRANULARITIES = [('detailed', 'Detailed'), ('general', 'General')]

    input_type = serializers.ChoiceField(choices=INPUT_TYPES)
    form = serializers.ChoiceField(choices=FORM_TYPES)
    length = serializers.IntegerField(min_value=1, max_value=30)
    language = serializers.ChoiceField(choices=LANGUAGES)
    granularity = serializers.ChoiceField(choices=GRANULARITIES)
    text = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False, allow_blank=True)

    def validate(self, data):
        input_type = data.get('input_type')

        if input_type == 'text' and not data.get('text'):
            raise serializers.ValidationError("Text input is required when 'input_type' is 'text'.")
        if input_type == 'file' and not data.get('file'):
            raise serializers.ValidationError("A file must be uploaded when 'input_type' is 'file'.")
        if input_type == 'url' and not data.get('url'):
            raise serializers.ValidationError("A valid URL is required when 'input_type' is 'url'.")

        return data