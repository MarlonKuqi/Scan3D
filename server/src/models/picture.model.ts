export class Picture {
    date: number;
    sent: boolean;
    base64: string;
    constructor() {
        this.date = 0;
        this.sent = true;
        this.base64 = '';
    }
   async exportToFile() {
        // to be written
        const fs = require('fs');
        /*const matches = this.base64.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
        let response: any;

        if (matches.length !== 3) {
            console.log('erreur in base64 format')
            return;
        }
        response.type = matches[1];
        response.data = new Buffer(matches[2], 'base64');*/
        fs.writeFile(this.date + '.jpg', this.base64, (err) => { console.log('erreur in exporting to file')});
    }
}
