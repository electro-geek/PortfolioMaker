from django import forms
from .models import PortfolioRequest


class ResumeUploadForm(forms.ModelForm):
    """Form for uploading resume PDF"""
    
    class Meta:
        model = PortfolioRequest
        fields = ['resume_file']
        widgets = {
            'resume_file': forms.FileInput(attrs={
                'accept': 'application/pdf',
                'class': 'hidden',
                'id': 'resume-upload'
            })
        }
    
    def clean_resume_file(self):
        file = self.cleaned_data.get('resume_file')
        
        if file:
            # Check file extension
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            
            # Check file size (limit to 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB.')
        
        return file
