function filterCheckList(e) {
  $(e).parent().parent().find("label").show();
  $(e).parent().parent().find("label:not(:contains(\""+$(e).val()+"\"))").hide();
}
