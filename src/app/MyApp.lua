
require("config")
require("cocos.init")
require("framework.init")

local MyApp = class("MyApp", cc.mvc.AppBase)

function MyApp:ctor()
    MyApp.super.ctor(self)
end

function MyApp:run()
    cc.FileUtils:getInstance():addSearchPath("res/")
    --cc.LuaLoadChunksFromZIP("game.zip")
    -- self:enterScene("MainScene")
    local updateLayer = require("app.update.UpdateLayer").new()
    display.replaceScene(updateLayer)
end

return MyApp
