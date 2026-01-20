function autoComplete(inputSelector) {
    var inputElement = $(inputSelector);
    var buscaUrl = inputElement.data('url');
    var hiddenSelector = inputElement.data('hidden');

    $(inputSelector).autocomplete({
        minLength: 1,
        source: function(request, response) {
            $.ajax({
                url: buscaUrl,
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item.nome,
                            value: item.nome,
                            id: item.id
                        };
                    }));
                }
            });
        },
        select: function(event, ui) {
            $(hiddenSelector).val(ui.item.id);
        }
    });
}

// ================= IMAGEM =================

function loadImage(base64Image, target_canvas) {
    var img = new Image();
    img.src = base64Image;

    img.onload = function() {
        const canvas = document.getElementById(target_canvas);
        const ctx = canvas.getContext('2d');
        var canvasWidth = canvas.width;
        var canvasHeight = canvas.height;

        var imgWidth = img.width;
        var imgHeight = img.height;

        var scaleWidth = canvasWidth / imgWidth;
        var scaleHeight = canvasHeight / imgHeight;
        var scale = Math.min(scaleWidth, scaleHeight);

        var newWidth = imgWidth * scale;
        var newHeight = imgHeight * scale;

        var offsetX = (canvasWidth - newWidth) / 2;
        var offsetY = (canvasHeight - newHeight) / 2;

        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);
    };
}
