$( document ).ready(function() {

    $('#add_product').click(function(e) {
      e.preventDefault();
      // what is next item_set *number* -
      var item_rows = $('.item_row').length;
      // clone of last item_row
      var $itemClone = $('.item_row:last').clone(true);

      $('.remove_item').attr('disabled', true);
      $('#id_item_set-TOTAL_FORMS').val(item_rows+1);
      $itemClone.find('[name$="-product"]').attr('id', 'id_item_set-'+item_rows+'-product').attr('name', 'item_set-'+$('.item_row').length+'-product').val('');
      $itemClone.find('[name$="-quantity"]').attr('id', 'id_item_set-'+item_rows+'-quantity').attr('name', 'item_set-'+$('.item_row').length+'-quantity').val(1);
      $itemClone.find('[name$="-price"]').attr('id', 'id_item_set-'+item_rows+'-price').attr('name', 'item_set-'+$('.item_row').length+'-price').val('');
      $itemClone.find('[name$="-unit"]').attr('id', 'id_item_set-'+item_rows+'-unit').attr('name', 'item_set-'+$('.item_row').length+'-unit').val('');
      $itemClone.find('[name$="-invoice"]').attr('id', 'id_item_set-'+item_rows+'-invoice').attr('name', 'item_set-'+$('.item_row').length+'-invoice').val('');
      $itemClone.find('[name$="-id"]').attr('id', 'id_item_set-'+item_rows+'-id').attr('name', 'item_set-'+$('.item_row').length+'-id').val('');
      $itemClone.find('.remove_item').attr('disabled', false);

      $('#items_row').append($itemClone);
    });

    $('.remove_item').click(function(e){
      e.preventDefault();
      if ($('.item_row').length > 1) {
        $(this).parents('.item_row').find(':checkbox').prop('checked', true);
        $(this).parents('.item_row').hide();
        $('.remove_item:last').attr('disabled', false);
      }
    });

    // new buyer
    $('#id_invoice_b_fk').append($('<option>', {
      value: 'newBuyer',
      text: 'DODAJ NOWEGO NABYWCĘ'
    })).on('change', function(e) {
      e.preventDefault();
      var selectedOpt = $(this).find(':selected').val();
      if (selectedOpt === 'newBuyer') {
        $('#buyerModal').modal('show');
        $(this).val(0);
      }
    });

});
