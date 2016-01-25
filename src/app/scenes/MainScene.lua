
local MainScene = class("MainScene", function()
    return display.newScene("MainScene")
end)

function MainScene:ctor()
	-- cc.LuaLoadChunksFromZIP("game.zip")
    cc.ui.UILabel.new({
            UILabelType = 2, text = "Hello, World", size = 64})
        :align(display.CENTER, display.cx, display.cy)
        :addTo(self)

    -->>>>>>>>>>>>>>>>>>>>>>>>>> pbc test
    import "protobuf-pbc.protobuf"
    --  Register
    local fullPath = cc.FileUtils:getInstance():fullPathForFilename("protobuf-pbc/addressbook.pb")
	-- local fullPath = cc.FileUtils:getInstance():fullPathForFilename("src/config.lua")
    printf("FullPath:%s",fullPath)
    -- local addr = cc.FileUtils:getInstance():getFileData("protobuf-pbc/addressbook.pb","rb",0)
    local addr = io.open(fullPath,"rb")
    local buffer = bsReadFile(fullPath)
    -- buffer = addr:read "*a"
    -- addr:close()
    protobuf.register(buffer)
    -- or
    -- protobuf.register_file "/Users/liming/Documents/work/cocos2d-x-3.8/projects/MyGame/src/app/proto/addressbook.pb"
    
    
    local addressbook = {
        name = "Alice",
        id = 12345,
        phone = {
            { number = "1301234567" },
            { number = "87654321", type = "WORK" },
        }
    }
    local code = protobuf.encode("tutorial.Person", addressbook)
    local decode = protobuf.decode("tutorial.Person" , code)
    printf("Name:%s Id:%d",decode.name,decode.id)

end

function MainScene:onEnter()
end

function MainScene:onExit()
end

return MainScene
