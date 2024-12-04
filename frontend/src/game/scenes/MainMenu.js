import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class MainMenu extends Scene
{
    logoTween;

    constructor ()
    {
        super('MainMenu');
    }

    createContainer = (locX, locY, name) => {
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
    
        text1.setPosition(r.x-text1.width/2, r.y-text1.height/2);
        var c = this.add.container();
        c.add([r, text1]);
        c.setPosition((512-300) + (locY-1) * 50 + 25, (460+200) - (locX-1) * 50 - 25);

        return c;
    }

    create ()
    {
        this.add.grid(512, 460, 600, 400, 50, 50, 0xff0000, 1, 0x000000);
        var containers = this.game.registry.get('gameData')['message'];
        for(const c of containers) {
            var s = c[0];
            s = s.substr(1, s.length-2);
            const nums = s.split(',').map(num => Number(num));
            this.createContainer(nums[0], nums[1], c[2]);
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
