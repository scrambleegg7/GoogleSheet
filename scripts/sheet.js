function compare(a, b){
    var comparison = 0
  
    // reversal sort 
    if (a > b) {
      comparison = -1;
      
    } else if (b > a) {
      comparison = 1;
    }
  
    return comparison;
  }
  
  
  function myReadCSV_EMOut() {
    
  
    var url = 'https://drive.google.com/drive/folders/1qrcCgpmoB4lLqlL3nnaf6ZOMHVVTyW-7', // URL of Google Drive folder.
        paths = url.split('/'), // Separate URL into an array of strings by separating the string into substrings. 
        folderId = paths[paths.length - 1], // Get a last element of paths array.
        folder = DriveApp.getFolderById(folderId),
        files = folder.getFiles(),
        list = [],
        rowIndex = 1, // The starting row of a range.
        colIndex = 1, // The starting row of a column.
        ss, sheet,range,
        sheetName = 'シート1';
  
    var response = "出庫"
    var reg_out = /出庫*/;
    var reg_in = /入庫*/;
    
    while(files.hasNext()) {
      var file = files.next();
      Logger.log( file.toString() )
      
      
      var filestr = file.toString();
      matched_in = filestr.match(reg_in)
      matched_out = filestr.match(reg_out)
      if ( matched_out != null ) {
        Logger.log(  matched_out.length   )
        list.push( file.toString() )
      }
  
    }
    
    
    var sorted = list.sort(compare)
    latestFile = sorted[0]
    
    
    var file = DriveApp.getFilesByName( latestFile ).next();
    var data = file.getBlob().getDataAsString("Shift_JIS");
    var csvData = Utilities.parseCsv( data );
    
  
    
    //var sheet = SpreadsheetApp.getActiveSheet();
    sheet = onOpen("dailyOut")
    sheet.getRange(1, 1, csvData.length, csvData[0].length).setValues(csvData);
    
  }