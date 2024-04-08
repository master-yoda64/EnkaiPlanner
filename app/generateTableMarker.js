    
window.onload = function() {
    const imageContainer = document.getElementById('image-container');
    let activeCircle = null;
    let offsetX = 0;
    let offsetY = 0;

    fetch('tables.txt')
        .then(response => response.text())

        .then(data => {
            const strings = data.split(',');
            strings.forEach((string) => {
                const tableCircle = document.createElement('div');
                tableCircle.classList.add('table-circle');
                var ascii = (Number(string) + 65 - 1) + 1;
                tableCircle.textContent = String.fromCharCode(ascii);
                tableCircle.style.left = `${Number(string)*100}px`;
                tableCircle.style.top = `0px`;
        
                tableCircle.addEventListener('mousedown', (event) => {
                    activeCircle = tableCircle;
                    offsetX = event.clientX - parseInt(activeCircle.style.left);
                    offsetY = event.clientY - parseInt(activeCircle.style.top);
                });
    
                imageContainer.appendChild(tableCircle);        
            });
    })
    .catch(error => {
        console.error('エラー:', error);
    });


    document.addEventListener('mousemove', (event) => {
        if (activeCircle) {
            const x = event.clientX - offsetX;
            const y = event.clientY - offsetY;

            activeCircle.style.left = `${x}px`;
            activeCircle.style.top = `${y}px`;
        }
    });

    document.addEventListener('mouseup', () => {
        activeCircle = null;
    });
};