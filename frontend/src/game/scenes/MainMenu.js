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
    createContainer = (locX, locY, name, itemID, unload, weight) => {
        var color = 0x0000ff;
        // If unused return NULL
        if(name == "UNUSED")
            return;

        // If container named NAN set to gray
        if(name == "NAN") {
            name = "";
            color = 0x808080;
        }

        const text0 = this.add.text(0, 0, name, {
            fontSize: '0px',
            color: '#ffffff',
            fontFamily: 'Arial',
            align: 'center',
        });
        
        var fullname = name;
        // Crop name if too long to make it fit inside container
        if(name.length > 5) {
            name = name.substr(0, 5);
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

        // Add weight
        // Add text
        const weightNum = this.add.text(-5, 10, weight, {
            fontSize: '10px',
            color: '#ffffff',
            fontFamily: 'Arial',
            align: 'center',
        });

        if(name == "") {
            weightNum.setAlpha(0);
        }

        // Add location as 2nd text to send to backend
        let pos = '[' + locX + ',' + locY + ']';
        const text2 = this.add.text(0, 0, pos, {
            fontSize: '0px',
        });
    
        text1.setPosition(r.x-text1.width/2, r.y-text1.height/2);
        var c = this.add.container();
        c.add([r, text1, text2, text0, weightNum]);
            
        c.setPosition((512-300) + (locY-1) * 50 + 25, (460+200) - (locX-1) * 50 - 25);
        c.setInteractive(new Phaser.Geom.Rectangle(-25, -25, 50, 50), Phaser.Geom.Rectangle.Contains)

        const hoverText = this.add.text(0, 0, '', {
            fontSize: '12px',
            color: '#ffffff',
            backgroundColor: '#000000',
            fontFamily: 'Arial',
            align: 'center',
            padding: { left: 5, right: 5, top: 2, bottom: 2 },
            alpha: 0, // Initially hidden
        });
        hoverText.setDepth(10); // Ensure it stays on top of other elements
        
        // Add hover behavior
        c.on('pointerover', () => {
            hoverText.setAlpha(1); // Make hover text visible
            hoverText.setText(`Name: ${fullname}\nWeight: ${weight}\n`);
            hoverText.setPosition(c.x + 30, c.y - 30); // Position near the container
        });
        
        c.on('pointerout', () => {
            hoverText.setAlpha(0); // Hide hover text
        });
        
        c.on('pointermove', (pointer) => {
            // Update hover text position dynamically based on the container
            hoverText.setPosition(c.x + 30, c.y - 30);
        });

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

        this.add.image(300, 500, 'crane');

        this.craneLine = this.add.line(0, 0, 0, 0, 0, 0, 0x000000, 1).setLineWidth(3).setDepth(1);

        // Loading containers list
        const text1 = this.add.text(512, 100, "Containers:", {
            fontSize: '20px',
            color: '#ffffff',
            fontFamily: 'Arial',
            align: 'center',
        });

        // Align to center of grid
        text1.setPosition(text1.x - text1.width/2, text1.y);

        // List to hold containers to be loaded
        this.loadList = []

        // Render grid
        this.add.grid(512, 460, 600, 400, 50, 50, 0xff0000, 1, 0x000000);
        var containers = this.game.registry.get('gameData')['message'];
        console.log(containers)
        this.containersList = [];
        for(const c of containers) {
            // string containing position to array
            var s = c[0];
            s = s.substr(1, s.length-2);
            const nums = s.split(',').map(num => Number(num));
            const weight = Number(c[1].substr(1, c[1].length-2));
            var curr = this.createContainer(nums[0], nums[1], c[2], c[1], unload, weight);
            curr && this.containersList.push(curr)
        }
        console.log(`Containers list ${this.containersList}`)
        // Add input to containers
        for(let i = 0;i < this.containersList.length;i++) {
            // If container is clicked and has a name add it to unload list
            this.containersList[i].list[1]._text !== "" && this.containersList[i].on('pointerdown', (pointer, x, y, event) => {
                if(!unload.find(c => c === this.containersList[i].list[2]._text)) {
                    unload = unload.concat(this.containersList[i].list[2]._text);
                    this.containersList[i].list[0].setStrokeStyle(1, 0xFFFFFF);
                }
                else {
                    unload = unload.filter(c => c !== this.containersList[i].list[2]._text);
                    this.containersList[i].list[0].setStrokeStyle(1, 0x000000);
                }

                // State update from react
                var updateUnloadFunc = this.game.registry.get('updateUnload');
                updateUnloadFunc(unload);
                console.log(`Unload list: ${unload}`);
                console.log(this.containersList);
                event.stopPropagation();
            })
        }

        // Get moves for all containers
        this.events.on('move-container', (data) => {
            console.log(data);
            var containerMoves = data; 
            if(containerMoves) {
                this.containersToMove = containerMoves.ids;
                this.moves = containerMoves.paths;
                this.times = containerMoves.times;
                this.containerIndex = 0;
                this.movesIndex = 0;
                console.log("TEST STRing");
                console.log(`Moves: ${this.moves}`);
                console.log(`Times: ${this.times}`);
            }
            
        })
        
        // let id_count = 0;
        // Load new containers
        this.events.on('load-container', (data) => {
            const existingCount = this.loadList.filter(c => c.list[1]._text === data[0]).length;
            console.log(this.loadList.length)
            console.log(`Load List updated:`);
            this.loadList.forEach(item => console.log(item.list));

            if(this.loadList.length == 0) {
                var temp = this.createContainer(10, 1, data[0], 0, 0, data[1])
                this.loadList.push(temp)
                this.containersList.push(temp);
                temp.on('pointerdown', () => {
                    var cPos = temp.list[2]._text
                    this.loadList = this.loadList.filter(c => c.list[2]._text !== cPos)
                    // temp.destroy()
                    this.containersList = this.containersList.filter(c => c.active);
                    console.log(this.containersList);
                })
            }
            else {
                // Increment x position of last container to add to load list
                var pos = this.loadList[this.loadList.length-1].list[2]._text;
                pos = pos.substr(1, pos.length-2);
                var xPos = pos.split(',').map(num => Number(num))[1];
                
                console.log(`Same container: ${existingCount}`)
                
                var temp = this.createContainer(10, xPos+1, data[0], existingCount, 0, data[1]);
                this.loadList.push(temp)
                this.containersList.push(temp);
                temp.on('pointerdown', () => {
                    var cPos = temp.list[2]._text
                    this.loadList = this.loadList.filter(c => c.list[2]._text !== cPos)
                    // temp.destroy()
                    this.containersList = this.containersList.filter(c => c.active);
                    console.log(this.containersList);
                })
            }
        })

        // Move on to next container animation
        this.events.on('next-container', () => {
            // Get container destination
            var moves = this.moves[this.containerIndex];
            var xDest = this.gridToScreen(moves[moves.length - 1])[0] + 1;
            var yDest = this.gridToScreen(moves[moves.length - 1])[1] + 1;

            // Find container and set the position to the destination position
            this.containersList = this.containersList.filter(c => c.active);
            var selectedContainer = this.containersList.find(c => c.list[3]._text === this.containersToMove[this.containerIndex]);
            console.log(`The X and Y for next: ${xDest} -- ${yDest}`);
            selectedContainer.setPosition(xDest, yDest);
            var xi = +moves[moves.length - 1][0] + 1;
            var yi = +moves[moves.length - 1][1] + 1;
            selectedContainer.list[2]._text = '[' + xi + ',' + yi + ']';
            console.log(selectedContainer.list[2]._text);

            // If container is in unload position destroy it
            if(moves[moves.length - 1][0] == 8 && moves[moves.length - 1][1] == 0) {
                selectedContainer.destroy();
                this.containersList.filter(c => c.active);
                console.log(this.containersList);
            }

            // Increment container
            this.containerIndex = this.containerIndex+1;
            this.movesIndex = 0;

            // If all containers have been moved set movesIndex to -1 to prevent update from running
            if(this.containerIndex >= this.containersToMove.length) {
                this.movesIndex = -1;
                unload = [];
                this.craneLine.setTo(0, 0, 0, 0);
            }
        })

        EventBus.emit('current-scene-ready', this);
    }

    update() {
        if(this.movesIndex > -1) {
            // console.log(`Container List in Update: ${this.containersToMove}`);
            this.containersList = this.containersList.filter(c => c.active);
            var selectedContainer = this.containersList.find(c => c.list[3]._text === this.containersToMove[this.containerIndex]);
            // var selectedContainer = this.containersToMove[this.containerIndex];
            this.craneLine.setTo(selectedContainer.x, selectedContainer.y-25, selectedContainer.x, 93);
            var moves = this.moves[this.containerIndex];
            var xDest = this.gridToScreen(moves[this.movesIndex])[0];
            var yDest = this.gridToScreen(moves[this.movesIndex])[1];
            if(!(selectedContainer.x === xDest
            && selectedContainer.y === yDest)) {
                if(selectedContainer.x < xDest) {
                    selectedContainer.setPosition(selectedContainer.x+1, selectedContainer.y)
                }

                if(selectedContainer.x > xDest) {
                    selectedContainer.setPosition(selectedContainer.x-1, selectedContainer.y)
                }

                if(selectedContainer.y < yDest) {
                    selectedContainer.setPosition(selectedContainer.x, selectedContainer.y+1)
                }

                if(selectedContainer.y > yDest) {
                    selectedContainer.setPosition(selectedContainer.x, selectedContainer.y-1)
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
