async function getWordlists() {
    let response = await fetch('/api/get_wordlists');
    let txt = await response.json();
    return txt
    // .then(res => res.text())
}

// send file
async function decryptLSBAes(data) {
    const requestOptions = {
        method: 'POST',
        body: data
    };

    let response = await fetch('/api/lsb_aes', requestOptions);
    return response.text();
}

// send file
async function reverse_file(data) {
    const requestOptions = {
        method: 'POST',
        body: data
    };

    await fetch('/api/reverse_file', requestOptions);
}

async function download_file_template(data) {
    const requestOptions = {
        method: 'POST',
        body: data
    };

    let response = await fetch('/api/reverse_file', requestOptions);
    const contentDisposition = response.headers.get('content-disposition');
    const filename = contentDisposition.split('filename=')[1];
    const name = filename.trim('').replace(/^"|"$/g, '')
    return [response.blob(), name]
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

export {getWordlists, decryptAes, decryptLSBAes, WordFrequecy, reverse_file}
