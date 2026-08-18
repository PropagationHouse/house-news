/**
 * House Dispatch — subscriber collector
 * --------------------------------------
 * This script turns a Google Sheet into your subscriber store.
 * No mailing platform. Your data, your sheet.
 *
 * SETUP (3 minutes):
 *   1. Create a Google Sheet (drive.google.com → Blank spreadsheet).
 *      Name it "House Dispatch Subscribers" (or anything).
 *   2. Extensions → Apps Script. Delete the placeholder code, paste this file.
 *   3. Click Deploy → New deployment → Web app:
 *        - Description: "house dispatch subscriber collector"
 *        - Execute as:  Me
 *        - Who has access: Anyone
 *        - Click Deploy, authorize (it's your own sheet), copy the Web app URL.
 *   4. Paste that URL into subscribe.html as SCRIPT_URL (search for SCRIPT_URL).
 *
 * The script creates a "subscribers" tab with columns:
 *   Timestamp | Email | Source | Status
 * Rows are deduped by email. That sheet is your list.
 */

var SHEET_NAME = 'subscribers';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var email = String(data.email || '').trim().toLowerCase();
    var source = String(data.source || 'subscribe.html').slice(0, 200);

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return respond_({ ok: false, error: 'invalid email' }, 400);
    }

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Email', 'Source', 'Status']);
      sheet.getRange(1, 1, 1, 4).setFontWeight('bold');
    }

    // Dedupe against existing rows (email lives in column B)
    var lastRow = Math.max(sheet.getLastRow() - 1, 0);
    var existing = lastRow
      ? sheet.getRange(2, 2, lastRow, 1).getValues().map(function (r) { return String(r[0]).trim().toLowerCase(); })
      : [];
    if (existing.indexOf(email) !== -1) {
      return respond_({ ok: true, duplicate: true });
    }

    sheet.appendRow([new Date(), email, source, 'subscribed']);
    return respond_({ ok: true });
  } catch (err) {
    return respond_({ ok: false, error: String(err) }, 500);
  }
}

function respond_(obj, code) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
