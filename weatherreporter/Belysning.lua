for key,value in pairs(content) do print(key,value) end

Mediaroom_window = 'uuid=76697596-8e50-487f-9217-91b6db4ad171'

turnOn = function (lamp)
    sendCmd ("On", lamp)
end

turnOff = function (lamp)
    sendCmd ("Off", lamp)
end

sendCmd = function (cmd, lamp)
    command = 'command=' ..cmd
    dev='uuid=' .. lamp
    sendMessage ('command=settemperature', 'mode=cool', thermostat)
end


if content.subject == "event.environment.timechanged" then
        -- Weekday
        if content.weekday < 6 then
                if content.hour == 07 and content.minute == 00 then     -- 07:00
                        turnOn(Mediaroom_window)
                end
                if content.hour == 08 and content.minute == 15 then     -- 08:15
                        turnOff(Mediaroom_window)
                end
        end

        -- Weekend
        if content.weekday >= 6 then
                if content.hour == 08 and content.minute == 30 then     -- 08:30
                        turnOn(Mediaroom_window)
                end
                if content.hour == 09 and content.minute == 00 then     -- 09:00
                        turnOff(Mediaroom_window)
                end
                if content.hour == 10 and content.minute == 25 then     -- 10:25
                        turnOff(Mediaroom_window)
                end

        end

end