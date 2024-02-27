from django import forms

from books.models import BookReview


class BookUpdateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    isbn = forms.CharField(label='ISBN', max_length=13)
    image = forms.ImageField(label='Image')

    def save(self, book):
        book.title = self.cleaned_data['title']
        book.description = self.cleaned_data['description']
        book.isbn = self.cleaned_data['isbn']
        book.image = self.cleaned_data['image']
        book.save()

        return book



class AddReviewForm(forms.Form):
    stars_given = forms.IntegerField(label='Stars', min_value=1, max_value=5)
    comment = forms.CharField(label='Comment', widget=forms.Textarea)

    def save(self, book, user):
        book_review = BookReview.objects.create(
            user=user,
            book=book,
            comment=self.cleaned_data['comment'],
            stars_given=self.cleaned_data['stars_given']
        )
        return book_review
