class OperationError extends Error {
    constructor(message) {
        // 调用父类的构造函数，并传递错误信息给它
        super(message);

        // 设置错误的名称，这可以用来区分不同类型的错误
        this.name = "OperationError";

        // 可选：如果需要，可以在这里设置其他属性或方法
    }
}


class RailFenceCipherTypeMDecode {

    run(input, args) {
        const [key, offset] = args;

        const cipher = input;

        if (key < 2) {
            throw new OperationError("Key has to be bigger than 2");
        } else if (key > cipher.length) {
            throw new OperationError("Key should be smaller than the cipher's length");
        }

        if (offset < 0) {
            throw new OperationError("Offset has to be a positive integer");
        }

        const cycle = (key - 1) * 2;
        const plaintext = new Array(cipher.length);

        let j = 0;
        let x, y;

        for (y = 0; y < key; y++) {
            for (x = 0; x < cipher.length; x++) {
                if ((y + x + offset + key - 1) % cycle === 0 || (y - (x + key - 1) - offset) % cycle === 0) {
                    plaintext[x] = cipher[j++];
                }
            }
        }

        return plaintext.join("").trim();
    }

}

export default RailFenceCipherTypeMDecode;

// let decode = new RailFenceCipherTypeMDecode();
// let res = decode.run("a2lg13f{}", [3, 0]);
// console.assert(res === "flag{123}")
// console.assert(decode.run("{a797g7441b553}aef9c6b2el7db607e5f3aae", [5, 0]) === "flag{7e73df4a49ba6c17b60a7b5952ee5e37}")
