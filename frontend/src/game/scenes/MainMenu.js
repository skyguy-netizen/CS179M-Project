import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class MainMenu extends Scene
{
    logoTween;

    constructor ()
    {
        super('MainMenu');
    }

    // Creates individual container
    createContainer = (locX, locY, name, itemID, unload) => {
        var color = 0x0000ff;
        // If unused return NULL
        if(name == "UNUSED")
            return;

        // If container named NAN set to gray
        if(name == "NAN") {
            name = "";
            color = 0x808080;
        }

        // Crop name if too long to make it fit inside container
        if(name.length > 3) {
            name = name.substr(0, 3);
            name = name.concat("...");
        }

        // Create rectangle of 50 x 50 with outline
        var r = this.add.rectangle(0, 0, 50, 50, color, 1);
        r.setStrokeStyle(1, 0x000000);

        // Add text
        const text1 = this.add.text(0, 0, name, {
            fontSize: '15px',
            color: '#ffffff',
            fontFamily: 'Arial',
            align: 'center',
        });

        // Add location as 2nd text to send to backend
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

    // Converts grid coordinates to screen coordinates
    gridToScreen = (arr) => {
        var curr = [];
        curr.push((512-300) + (arr[1]) * 50 + 25);
        curr.push((460+200) - (arr[0]) * 50 - 25);
        return [(512-300) + (arr[1]) * 50 + 25, (460+200) - (arr[0]) * 50 - 25];
    }

    create ()
    {
        var unload = [];
        this.add.grid(512, 460, 600, 400, 50, 50, 0xff0000, 1, 0x000000);
        var containers = this.game.registry.get('gameData')['message'];
        this.containersList = [];

        for(const c of containers) {
            var s = c[0];
            s = s.substr(1, s.length-2);
            const nums = s.split(',').map(num => Number(num));
            var curr = this.createContainer(nums[0], nums[1], c[2], c[1], unload);
            curr && this.containersList.push(curr)
        }

        for(let i = 0;i < this.containersList.length;i++) {
            this.containersList[i].list[1]._text !== "" && this.containersList[i].on('pointerdown', (pointer, x, y, event) => {
                if(!unload.find(c => c === this.containersList[i].list[2]._text))
                    unload = unload.concat(this.containersList[i].list[2]._text);
                else
                    unload = unload.filter(c => c !== this.containersList[i].list[2]._text);
                var updateUnloadFunc = this.game.registry.get('updateUnload');
                updateUnloadFunc(unload);
                console.log(`Unload list: ${unload}`);
                event.stopPropagation();
            })
        }

        this.events.on('move-container', (data) => {
            console.log(data);
            var containerMoves = data; 
            if(containerMoves) {
                this.containersToMove = containerMoves.ids;
                this.moves = containerMoves.paths;
                this.times = containerMoves.times;
                this.containerIndex = 0;
                this.movesIndex = 0;
            }
        })
        
        this.events.on('next-container', () => {
            // Get container destination
            var moves = this.moves[this.containerIndex];
            var xDest = this.gridToScreen(moves[moves.length-1])[0];
            var yDest = this.gridToScreen(moves[moves.length-1])[1];

            // Find container and set the position to the destination position
            var selectedContainer = this.containersList.find(c => c.list[1]._text === this.containersToMove[this.containerIndex]);
            selectedContainer.setPosition(xDest, yDest);

            // If container is in unload position destroy it
            if(moves[moves.length-1][0] == 8 && moves[moves.length-1][1] == 0) {
                selectedContainer.destroy();
            }

            // Increment container
            this.containerIndex = this.containerIndex+1;
            this.movesIndex = 0;

            // If all containers have been moved set movesIndex to -1 to prevent update from running
            if(this.containerIndex >= this.containersToMove.length) {
                this.movesIndex = -1;
            }
        })

        EventBus.emit('current-scene-ready', this);
    }

    update() {
        if(this.movesIndex > -1) {
            var selectedContainer = this.containersList.find(c => c.list[1]._text === this.containersToMove[this.containerIndex]);
            var moves = this.moves[this.containerIndex];
            var xDest = this.gridToScreen(moves[this.movesIndex])[0];
            var yDest = this.gridToScreen(moves[this.movesIndex])[1];
            if(!(selectedContainer.x === xDest
            && selectedContainer.y === yDest)) {
                if(selectedContainer.x < xDest) {
                    selectedContainer.setPosition(selectedContainer.x+2, selectedContainer.y)
                }

                if(selectedContainer.x > xDest) {
                    selectedContainer.setPosition(selectedContainer.x-2, selectedContainer.y)
                }

                if(selectedContainer.y < yDest) {
                    selectedContainer.setPosition(selectedContainer.x, selectedContainer.y+2)
                }

                if(selectedContainer.y > yDest) {
                    selectedContainer.setPosition(selectedContainer.x, selectedContainer.y-2)
                }
            }
            else {
                this.movesIndex = this.movesIndex+1;
                if(this.movesIndex >= moves.length) {
                    this.movesIndex = 0;
                    var originalPosition = selectedContainer.list[2]._text.substr(1, selectedContainer.list[2]._text.length-2);
                    const nums = originalPosition.split(',').map(num => Number(num)-1);
                    selectedContainer.setPosition(this.gridToScreen(nums)[0], this.gridToScreen(nums)[1]);
                }
            }
        }
    }

    testFunc = () => {
        console.log("test");
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
