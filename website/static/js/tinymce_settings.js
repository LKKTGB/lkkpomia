tinymce.init({
  selector: 'textarea',
  language: 'zh_TW',
  height: 500,
  menubar: false,
  plugins: [
    'lists link image media paste wordcount'
  ],
  toolbar: 'formatselect bold italic | numlist bullist | alignleft aligncenter | link image media',

  // formatselect
  block_formats: 'Paragraph=p;Header 1=h1;Header 2=h2',
  // link
  link_title: false,
  // media
  media_alt_source: false,
  media_poster: false,
  media_dimensions: false,
  // paste
  paste_as_text: true,

  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//www.tinymce.com/css/codepen.min.css']
});
