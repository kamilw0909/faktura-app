$( document ).ready(function() {

    $('form').on('click', '#add_product', function(e) {
      e.preventDefault();
      // what is next item_set *number* -
      var item_rows = $('.item_row').length;
      // clone of first item_row
      var $itemClone = $('.item_row:first').clone(true);

      $('#id_item_set-TOTAL_FORMS').val(item_rows+1);
      $itemClone.find('[name$="-product"]').attr('id', 'id_item_set-'+item_rows+'-product').attr('name', 'item_set-'+$('.item_row').length+'-product').val('');
      $itemClone.find('[name$="-quantity"]').attr('id', 'id_item_set-'+item_rows+'-quantity').attr('name', 'item_set-'+$('.item_row').length+'-quantity').val(1);
      $itemClone.find('[name$="-price"]').attr('id', 'id_item_set-'+item_rows+'-price').attr('name', 'item_set-'+$('.item_row').length+'-price').val('');
      $itemClone.find('[name$="-unit"]').attr('id', 'id_item_set-'+item_rows+'-unit').attr('name', 'item_set-'+$('.item_row').length+'-unit').val('');
      $itemClone.find('[name$="-invoice"]').attr('id', 'id_item_set-'+item_rows+'-invoice').attr('name', 'item_set-'+$('.item_row').length+'-invoice').val('');
      $itemClone.find('[name$="-id"]').attr('id', 'id_item_set-'+item_rows+'-id').attr('name', 'item_set-'+$('.item_row').length+'-id').val('');

      $('#items_row').append($itemClone);
    });

    $('#items_row').on('click', '.remove_item', function(e){
      e.preventDefault();
      if ($('.item_row').length > 1) {
        $(this).parents('.item_row').find(':input').prop('required', false);
        $(this).parents('.item_row').find('select').prop('required', false);
        $(this).parents('.item_row').find(':checkbox').prop('checked', true);
        $(this).parents('.item_row').hide();
      }
    });

    // if item row is active editing
    // change to required all row field
    $('#items_row').on('change', '.item_row', function(){
        if ($(this).find(':text').val() !== '') {
            $(this).find(':input').prop('required', true);
            $(this).find('select').prop('required', true);
            $(this).find(':checkbox').prop('required', false);
        } else {
            $('.item_row :input').prop('required', false);
            $('.item_row select').prop('required', false);
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
