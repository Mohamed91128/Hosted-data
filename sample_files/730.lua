-- Counter-Strike 2 Plugin Configuration
-- Game ID: 730

local config = {
    game_name = "Counter-Strike 2",
    game_id = "730",
    version = "1.0.0",
    author = "Steam Game Manager",
    description = "CS2 game modification files",
    
    settings = {
        auto_load = true,
        enable_modifications = true,
        backup_original = true
    },
    
    files = {
        lua = "730.lua",
        json = "730.json",
        folder = "730",
        manifest = "730_manifest"
    }
}

-- Plugin initialization
function init_plugin()
    print("Initializing CS2 plugin...")
    -- Plugin initialization code here
    return true
end

-- Plugin cleanup
function cleanup_plugin()
    print("Cleaning up CS2 plugin...")
    -- Plugin cleanup code here
end

-- Export configuration
return config 