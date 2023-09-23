function generateHash() {
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 64; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters.charAt(randomIndex);
    }
    return result;
}

const json_data = JSON.parse(document.getElementById('json-data').textContent);

function delayLoop(iterations, delay) {
    let i = 0;
    function loop() {
        setTimeout(function () {
            value = (i / iterations) * 100;
            var progress_bar = document.getElementById("hash-progress").style.width = `${value}%`;
            document.getElementById("hash-text").innerHTML = `<b>nonce: [${i}]</b> ${generateHash()}`;
            document.getElementById("id_block_hash").value = generateHash();
            document.getElementById("nonce").value = i;
            i++;
            if (i <= iterations) {
                loop();
            }
            else {
                document.getElementById("hash-text").innerHTML = `<b>nonce: [${iterations}]</b> ${json_data["block_hash"]}`;
                document.getElementById("id_block_hash").value = json_data["block_hash"];
                document.getElementById("nonce").value = json_data["nonce"];
                document.getElementById("spinner").classList.add('d-none');
            }
        }, delay);
    }
    loop();
}
delayLoop(json_data["nonce"], 1);
