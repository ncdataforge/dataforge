function updateFileName() {
    const input = document.getElementById('file-input');
    const label = document.getElementById('selected-file');
    const fileName = input.files.length > 0 ? input.files[0].name : 'Ninguno';
    label.textContent = `Archivos seleccionados: ${fileName}`;
}

document.getElementById('uploadForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const loadingMessage = document.getElementById('loading');
    const dots = document.getElementById('dots');

    loadingMessage.style.display = 'block';

    let dotCount = 0;
    const dotAnimation = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        dots.textContent = '.'.repeat(dotCount);
    }, 500);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        clearInterval(dotAnimation);
        loadingMessage.style.display = 'none';

        if (data.output_file) {                    
            const downloadLink = `<a href="/download/${data.output_file}" download>Descargar resultados</a>`;                    
            document.getElementById('result').innerHTML = downloadLink;
        } else {
            document.getElementById('result').innerText = data.error;
        }

    } catch (error) {
        clearInterval(dotAnimation);
        loadingMessage.style.display = 'none';
        document.getElementById('result').innerText = 'Error en la conexión. Inténtalo de nuevo.';
        console.error(error);
    }
};