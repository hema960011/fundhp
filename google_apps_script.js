// Google Apps Script for handling GET (fetch) and POST (save) requests

function doGet(e) {
  try {
    var action = e.parameter.action;
    if (action === "sheets") {
      var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets().map(function(sheet) {
        return sheet.getName();
      });
      return ContentService.createTextOutput(JSON.stringify(sheets)).setMimeType(ContentService.MimeType.JSON);
    }
    
    var sheetName = e.parameter.sheetName;
    if (!sheetName) {
      return ContentService.createTextOutput(JSON.stringify({"error": "Missing sheetName parameter"})).setMimeType(ContentService.MimeType.JSON);
    }
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
      return ContentService.createTextOutput(JSON.stringify({"error": "Sheet not found"})).setMimeType(ContentService.MimeType.JSON);
    }
    
    var data = sheet.getDataRange().getValues();
    return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({"error": error.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    var params = JSON.parse(e.postData.contents);
    var sheetName = params.sheetName;
    var data = params.data; // Expected: array of arrays, e.g., [["value1", "value2"], ["value3", "value4"]]
    
    if (!sheetName || !data || !Array.isArray(data)) {
      return ContentService.createTextOutput(JSON.stringify({"error": "Invalid parameters"})).setMimeType(ContentService.MimeType.JSON);
    }
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    if (!sheet) {
      return ContentService.createTextOutput(JSON.stringify({"error": "Sheet not found"})).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Append the new data rows
    var startRow = sheet.getLastRow() + 1;
    var numRows = data.length;
    var numCols = data[0].length;
    sheet.getRange(startRow, 1, numRows, numCols).setValues(data);
    
    return ContentService.createTextOutput(JSON.stringify({"status": "success"})).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({"error": error.toString()})).setMimeType(ContentService.MimeType.JSON);
  }
}