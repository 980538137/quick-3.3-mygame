
local MainScene = class("MainScene", function()
    return display.newScene("MainScene")
end)

function MainScene:ctor()
    local node = cc.CSLoader:createNode("MainScene.csb")
    self:addChild(node)
	-- cc.LuaLoadChunksFromZIP("game.zip")
    cc.ui.UILabel.new({
            UILabelType = 2, text = "Hello, World", size = 64})
        :align(display.CENTER, display.cx, display.cy)
        :addTo(self)

    local bg = display.newSprite("enter_btn_click.png")
    -- make background sprite always align top
    bg:setPosition(display.cx, display.top - bg:getContentSize().height / 2)
    self:addChild(bg)

    -->>>>>>>>>>>>>>>>>>>>>>>>>> pbc test
    import "protobuf-pbc.protobuf"
    --  Register
    local fullPath = cc.FileUtils:getInstance():fullPathForFilename("protobuf-pbc/addressbook.pb")
	-- local fullPath = cc.FileUtils:getInstance():fullPathForFilename("src/config.lua")
    printf("FullPath:%s",fullPath)
    -- local addr = cc.FileUtils:getInstance():getFileData("protobuf-pbc/addressbook.pb","rb",0)
    -- local addr = io.open(fullPath,"rb")
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

    --lua_socket test
    SOCKET = require("app.network.socket").new("101.201.198.51",9080)
    SOCKET:connect()

    local function touchEvent(sender,eventType)
        if eventType == ccui.TouchEventType.began then

        elseif eventType == ccui.TouchEventType.moved then

        elseif eventType == ccui.TouchEventType.ended then
            SOCKET:disconnect()
        elseif eventType == ccui.TouchEventType.canceled then

        end
    end
    local btn = node:getChildByName("Button1")
    -- local login = ccui.Helper:seekWidgetByName(node, "EnterButton")
    btn:addTouchEventListener(touchEvent)


end

function MainScene:onEnter()
end

function MainScene:onExit()
end

return MainScene
