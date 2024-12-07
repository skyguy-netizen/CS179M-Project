import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class MainMenu extends Scene
{
    logoTween;

    constructor ()
    {
        super('MainMenu');
    }

    createContainer = (locX, locY, name, itemID, unload) => {
        var color = 0x0000ff;
        if(name == "UNUSED")
            return;

        if(name == "NAN") {
            name = "";
            color = 0x808080;
        }
        if(name.length > 3) {
            name = name.substr(0, 3);
            name = name.concat("...");
        }
        var r = this.add.rectangle(0, 0, 50, 50, color, 1);
        r.setStrokeStyle(1, 0x000000);

        const text1 = this.add.text(0, 0, name, {
            fontSize: '15px',
            color: '#ffffff',
            fontFamily: 'Arial',
            align: 'center',
        });

        let pos = '[' + locX + ',' + locY + ']';
        const text2 = this.add.text(0, 0, pos, {
            fontSize: '0px',
        });
    
        text1.setPosition(r.x-text1.width/2, r.y-text1.height/2);
        var c = this.add.container();
        c.add([r, text1, text2]);

        c.setPosition((512-300) + (locY-1) * 50 + 25, (460+200) - (locX-1) * 50 - 25);
        c.setInteractive(new Phaser.Geom.Rectangle(-25, -25, 50, 50), Phaser.Geom.Rectangle.Contains)

        return c;
    }

    create ()
    {
        var unload = [];
        var load = [];
        this.add.grid(512, 460, 600, 400, 50, 50, 0xff0000, 1, 0x000000);
        var containers = this.game.registry.get('gameData')['message'];
        var containersList = [];

        for(const c of containers) {
            var s = c[0];
            s = s.substr(1, s.length-2);
            const nums = s.split(',').map(num => Number(num));
            var curr = this.createContainer(nums[0], nums[1], c[2], c[1], unload);
            curr && containersList.push(curr)
        }

        for(let i = 0;i < containersList.length;i++) {
            containersList[i].list[1]._text !== "" && containersList[i].on('pointerdown', (pointer, x, y, event) => {
                if(!unload.find(c => c === containersList[i].list[2]._text))
                    unload = unload.concat(containersList[i].list[2]._text);
                else
                    unload = unload.filter(c => c !== containersList[i].list[2]._text);
                var updateUnloadFunc = this.game.registry.get('updateUnload');
                updateUnloadFunc(unload);
                console.log(`Unload list: ${unload}`);
                event.stopPropagation();
            })
        }
        
        EventBus.emit('current-scene-ready', this);
    }

    changeScene ()
    {
        if (this.logoTween)
        {
            this.logoTween.stop();
            this.logoTween = null;
        }

        this.scene.start('Game');
    }
}
