async function getWordlists() {
    let response = await fetch('/api/get_wordlists');
    let txt = await response.json();
    return txt
    // .then(res => res.text())
}

async function decryptLSBAes(data) {
    const requestOptions = {
        method: 'POST',
        body: data
    };

    let response = await fetch('/api/lsb_aes', requestOptions);
    return response.text();
}
async function WordFrequecy(data) {
    const requestOptions = {
        method: 'POST',
        body: data
    };

    let response = await fetch('/api/frequency', requestOptions);
    return response.text();
}
async function decryptAes(data) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    let response = await fetch('/api/aes', requestOptions);
    return response.text();
}

export {getWordlists, decryptAes,decryptLSBAes, WordFrequecy}
