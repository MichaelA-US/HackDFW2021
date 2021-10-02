function getRandomLetter() {
                            var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                            var result = '';
                            const randomChar = alphabet[Math.floor(Math.random() * alphabet.length)]
                            return randomChar;
                        }