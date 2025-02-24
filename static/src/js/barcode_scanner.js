/** @odoo-module **/

odoo.define('barcode_order_line.barcode_scanner', [], function (require) {
    "use strict";

    const Quagga = window.Quagga;

    function startBarcodeScanner() {
        const scannerTarget = document.getElementById("barcode-scanner");
        if (!scannerTarget) {
            console.warn("No se encontró el elemento #barcode-scanner, reintentando...");
            setTimeout(startBarcodeScanner, 500);
            return;
        }
        if (!Quagga) {
            console.error("QuaggaJS no está disponible");
            return;
        }
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: scannerTarget,
                constraints: {
                    facingMode: "environment"
                }
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader", "upc_reader"]
            }
        }, function (err) {
            if (err) {
                console.error(err);
                return;
            }
            console.log("QuaggaJS inicializado, iniciando escaneo...");
            Quagga.start();
        });

        Quagga.onDetected(function (result) {
            if (result && result.codeResult && result.codeResult.code) {
                const code = result.codeResult.code;
                console.log("Código detectado:", code);
                // Usar un selector sencillo que busque el input del campo barcode
                const barcodeField = document.querySelector("input[name='barcode']");
                if (barcodeField) {
                    barcodeField.value = code;
                    barcodeField.dispatchEvent(new Event('change'));
                } else {
                    console.error("No se encontró el input para el campo barcode");
                }
                // Simular clic en el botón de agregar
                const processButton = document.querySelector("button[name='action_process_barcode']");
                if (processButton) {
                    processButton.click();
                }
                Quagga.stop();
            }
        });

        const stopButton = document.getElementById("stop-scanner");
        if (stopButton) {
            stopButton.addEventListener("click", function () {
                Quagga.stop();
            });
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        startBarcodeScanner();
    });

    return {
        startBarcodeScanner: startBarcodeScanner,
    };
});
