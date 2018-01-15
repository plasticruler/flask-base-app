$(document).ready(function()
{
  $('.datetimepicker').datetimepicker(
    {
      format: 'YYYY-MM-DD H:mm:ss'
    }
  );
});

function processPriceData(d,e){
  if (d.Type==1)
  {
    console.error('Error on price retrieval');
    return;
  }
  console.log(d.USD);
  console.log(e);
  $(e).html('USD:' + d.USD);  
}
function getPrice(code, target)
{
  $.ajax({
          dataType:"json",
          url:`https://min-api.cryptocompare.com/data/price?fsym=${code}&tsyms=USD,EUR`
        }
  ).done((d,t)=>{
                  if (d.Type==1)
                  {
                    console.error('Error on price retrieval');
                    return;
                  }
                  $(target).html('$' + d.USD);
                }
 );
}