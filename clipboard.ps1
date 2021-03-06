

function Check-Clipboard{
    $image = Get-Clipboard -Format Image
    if($image -eq $null){
        "No picture on the clipboard!"
        exit(1)
    }
}



function Save-Clipboard{
    $image = Get-Clipboard -Format Image
    try{
        $image.Save($args[0 ])
    }catch{
        "No picture on the clipboard!"
        exit(1)
    }
    "The picture has been saved from the clipboard!"
}


if ($args[0] -eq "-c"){
    Check-Clipboard
}elseif ($args[0] -eq "-s") {
    Save-Clipboard $args[1]
}