from django import forms
from .models import Member

class MemberProfileForm(forms.ModelForm):
    # Custom fields for better UX
    roles = forms.MultipleChoiceField(
        choices=Member.ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Your Roles"
    )
    
    class Meta:
        model = Member
        fields = [
            'name', 'year', 'major', 'minor', 'birthday', 'home', 
            'quote', 'favorite_thing_1', 'favorite_thing_2', 'favorite_thing_3',
            'favorite_dartmouth_tradition', 'fun_fact', 'picture'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'minor': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD'}),
            'home': forms.TextInput(attrs={'class': 'form-control'}),
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'favorite_thing_1': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_thing_2': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_thing_3': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_dartmouth_tradition': forms.TextInput(attrs={'class': 'form-control'}),
            'fun_fact': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'picture': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for roles checkboxes
        if self.instance and self.instance.pk:
            initial_roles = []
            if self.instance.dev: initial_roles.append('dev')
            if self.instance.des: initial_roles.append('des')
            if self.instance.pm: initial_roles.append('pm')
            if self.instance.core: initial_roles.append('core')
            if self.instance.mentor: initial_roles.append('mentor')
            self.fields['roles'].initial = initial_roles
    
    def save(self, commit=True):
        member = super().save(commit=False)
        
        # Handle roles from checkboxes
        selected_roles = self.cleaned_data.get('roles', [])
        member.dev = 'dev' in selected_roles
        member.des = 'des' in selected_roles
        member.pm = 'pm' in selected_roles
        member.core = 'core' in selected_roles
        member.mentor = 'mentor' in selected_roles
        
        if commit:
            member.save()
        return member