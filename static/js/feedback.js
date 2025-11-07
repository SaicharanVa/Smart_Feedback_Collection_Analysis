document.addEventListener('DOMContentLoaded', function() {
    const feedbackForm = document.getElementById('feedbackForm');
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const feedbackResult = document.getElementById('feedbackResult');
    if (!feedbackForm || !imageInput) {
        return;
    }

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            if (file.size > 5 * 1024 * 1024) {
                alert('File size must be less than 5MB');
                imageInput.value = '';
                imagePreview.innerHTML = '';
                return;
            }

            const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                alert('Only PNG, JPG, JPEG, and GIF files are allowed');
                imageInput.value = '';
                imagePreview.innerHTML = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <p style="margin-top: 0.5rem; color: #27ae60;">✓ Image ready to upload</p>
                `;
            };
            reader.readAsDataURL(file);
        } else {
            imagePreview.innerHTML = '';
        }
    });

    feedbackForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(feedbackForm);

        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                feedbackResult.className = 'result-message success';
                feedbackResult.innerHTML = `
                    <strong>Success!</strong> ${data.message}<br>
                    <small>Sentiment Analysis: <strong>${data.sentiment}</strong> (Score: ${data.score.toFixed(3)})</small>
                `;
                feedbackForm.reset();
                imagePreview.innerHTML = '';
            } else {
                feedbackResult.className = 'result-message error';
                feedbackResult.innerHTML = `<strong>Error:</strong> ${data.message}`;
            }
        } catch (error) {
            feedbackResult.className = 'result-message error';
            feedbackResult.innerHTML = `<strong>Error:</strong> Failed to submit feedback. Please try again.`;
        }
    });
});

function openImageModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    modal.style.display = 'block';
    modalImg.src = imageSrc;
}
const modalClose = document.querySelector('.modal-close');
if (modalClose) {
    modalClose.addEventListener('click', function() {
        document.getElementById('imageModal').style.display = 'none';
    });
}

window.onclick = function(event) {
    const modal = document.getElementById('imageModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
