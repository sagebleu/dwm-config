#!/home/enz/bin/io_static

Ram := Object clone
Ram file := File with("/proc/meminfo") openForReading
Ram memTotal := nil
Ram memFree := nil
Ram buffers := nil
Ram cashed := nil
Ram update := method(
  self memTotal := self file readLine exSlice(9) asNumber
  self memFree := self file readLine exSlice(9) asNumber
  self buffers := self file readLine exSlice(9) asNumber
  self cashed := self file readLine exSlice(9) asNumber
)
Ram used := method(u,
  ((self memTotal - self memFree) - (self buffers + self cashed)) / u
)

Mocp := Object clone
Mocp format := "%artist\\ -\\ %song\\ [%ct/%tt]"
Mocp state := method(
  if(System runCommand("mocp -Q %state") exitStatus == 2,
    "OFF",
    System runCommand("mocp -Q %state") stdout exSlice(0, -1)
  )
)
Mocp getInfo := method(
  System runCommand("mocp -Q " .. self format) stdout exSlice(0, -1)
)

ram := Ram clone
mocp := Mocp clone

loop(
  #-----------  extract date
  date := Date now asString("%d %B %Y  %H:%M")
 
  #-----------  extract info from /proc/meminfo
  ram := Ram clone
  u := ram used(1024) round  # 1024 for MiB
  #---------- extract song being played

  m := if(mocp state == "OFF", "[off]",
       if(mocp state == "STOP", "[stop]",
          mocp getInfo))

  output := list(m,
            (u .. "/" .. ((ram memTotal / 1024) round) .. "MB"),
            date) join("  |  ")


  System system("xsetroot -name \"" .. output .. "\"")
  System sleep(0.5)
)


