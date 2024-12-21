// LabelPage.js
import { useParams } from 'react-router-dom';
import React, { useState } from 'react';
import axios from 'axios';


function AddLogins() {
  // URL dan parametrni olish
  const { param } = useParams();
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [capcha_id, setCapchaId] = useState("");
  const [capcha_value, setCapchaValue] = useState("");
  const [capcha_url, setCapchaUrl] = useState("");

  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };
  // const sleep = (ms) => {
  //   return new Promise((resolve) => setTimeout(resolve, ms));
  // };
  async function addLoginUser(login, parol, capcha_id, capcha_value) {
      // document.getElementById("content").style.height = "120px";
      try {
        // const loading = document.getElementById("loading");
        // loading.classList.remove("hidden")

        const res = await axios.post(`https://api.projectsplatform.uz/kundalikcom/register_logins/${param}`,
          {
            login,
            parol,
            capcha_id,
            capcha_value
          }
        );
        // loading.classList.add("hidden");
        console.log(res.data);
        if(res.data.how){
          return "✅ Bitta hisob aktiv qilindi";
        }else if(res.data.capcha){
          try{document.getElementById("capcha_page").classList.remove("login__body__captcha_hidden")}catch{}
          setCapchaId(res.data.capcha_id);
          setCapchaValue(res.data.capcha_value);
          setCapchaUrl(res.data.url);
          return "Rasmdagi raqamlarni kiriting";
        } else if(res.data !== false){
          return res.data.message;
        } else {
          return "Maktab mavjud emas";
        }
      } catch (e){
        console.log(e);
        return "❌ Internetga ulanmagansiz";
      }
  }

  const ruyxatdan_utish =  async () => {
    const username_input = document.getElementById("username-field");
    const password_input = document.getElementById("password-field");
    var username = username_input.value;
    var password = password_input.value;
    
    // document.getElementById("content").style.minHeight = "120px";
    const res = await addLoginUser(username, password, capcha_id, capcha_value);
    if(res === "✅ Bitta hisob aktiv qilindi"){
      alert(res);
      window.location.reload();
    }else{
      alert(res);
    }
    // console.clear();
  }










  return (
    <center>
      <div className="container" style={{
        maxWidth: '95%',
        width: '600px'
      }}>
      <link rel="stylesheet" href="https://static.emaktab.uz/styles/main/common.css?v=38675ba2" media="all" type="text/css"/>
      <link rel="stylesheet" href="https://static.emaktab.uz/blocks/blocks.css?v=c0cbef8b" media="all" type="text/css" />
      <div className="row">
        <div className="col-md-24 col-xs-24">
          <div className="article-area">
            <form className="login" method="POST">
              <input id="exceededAttempts" name="exceededAttempts" type="hidden" value="True" />
              <input id="ReturnUrl" name="ReturnUrl" type="hidden" value="" />
              <input id="FingerprintId" name="FingerprintId" type="hidden" value="" />

              <div className="login__header login__header_uz">
                <div className="row row_centered">
                  <div className="login__header-title col-md-12 col-xs-12">
                    <div className="login__header__text">
                      <h1 className="h1 h1_white">eMaktab hisobingizni faollashtirish</h1>
                    </div>
                  </div>
                  <div className="login__header-register-wrapper col-md-12 col-xs-12">
                  </div>
                </div>
              </div>

              <div className="login__body">
                <div className="login__body__hint login__body__hint_error-message login__body__hint_hidden">
                  <div className="message"></div>
                </div>

                <div className="login__error_message_mobile"></div>

                <div className="login__content login__content_mixed">
                  <div className="row row_centered login__form_shown">
                    <div className="login-body__field-wrapper col-md-12 col-xs-12">
                      <label className="label label_input-label label_bold">
                        <strong>Login</strong>
                        <input
                          id="username-field"
                          name="login"
                          className="input input__field input_full-width input_with-label-above input_line-height-28px login__body__input_login"
                          type="text"
                          autoComplete="on"
                          data-test-id="login-field"
                        />
                      </label>
                    </div>
                    <div className="login__body-hint-wrapper col-md-12 col-xs-12">
                      <div className="login__body__hint login__body__hint_login login__body__hint_hidden">
                        <div className="yellow-hint yellow-hint_right">
                          <div className="yellow-hint__wrapper">Loginingizni kiriting.</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="row row_centered login__form_shown">
                    <div className="login-body__field-wrapper col-md-12 col-xs-12">
                      <label className="label label_input-label label_bold">
                        <strong>Parol</strong>
                        <div
                          id="pass-visibility-button"
                          className={passwordVisible ? 'hide-pass-button' : 'show-pass-button'}
                          onClick={togglePasswordVisibility}
                        ></div>
                        <input
                          name="password"
                          id="password-field"
                          className="input input__field input_full-width input_with-label-above input_line-height-28px login__body__input_password"
                          type={passwordVisible ? 'text' : 'password'}
                          autoComplete="on"
                          data-test-id="password-field"
                        />
                      </label>
                    </div>
                    <div className="login__body-hint-wrapper col-md-12 col-xs-12">
                      <div className="login__body__hint login__body__hint_password login__body__hint_hidden">
                        <div className="yellow-hint yellow-hint_right">
                          <div className="yellow-hint__wrapper">Parolni kiriting.</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div id="capcha_page" className="login__body__captcha login__body__captcha_hidden login__form_shown">
                    <div className="row row_centered">
                      <div className="login__captcha-wrapper col-ms-12 col-xs-12">
                        <div className="captcha" name="captcha">
                          <div className="row">
                            <div className="col-ms-24 col-xs-24">
                              <label className="label label_bold label_input-label label_display-block label_font-size-14 label_">
                                Rasmdagi belgilarni kiriting
                              </label>
                              <img alt="captcha image" id='capcha-image' className="captcha__image" src={capcha_url} />
                              <input type="text" onChange={(e) => setCapchaValue(e.target.value)} id="capcha_value_input" name="Captcha.Id" className="captcha__value input input__field input_full-width input_with-label-above input_line-height-28px login__body__input_login" />
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="login__captcha-error-wrapper col-md-12 col-xs-12">
                        <div className="login__body__captcha__error">
                          <div className="yellow-hint yellow-hint_to-left-20 yellow-hint_right yellow-hint_captcha-hint yellow-hint_hidden">
                            <div className="yellow-hint__wrapper"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="row row_centered">
                    <div className="login-body__field-wrapper col-md-6 col-xs-6 login__form_shown">
                      <p
                        onClick={ruyxatdan_utish}
                        style={{paddingTop: "10px", userSelect: "none"}}
                        className="login__submit button button_light-green button_top-10 button_full-width"
                        data-test-id="login-button">Tizimga kiring</p>
                    </div>

                    <div className="login-body__field-wrapper login-body__field-wrapper_show-form-btn login__form_shown">
                      <button type="button" className="button button_show-form-btn">"Kundalik" orqali kiring</button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    </center>
  );
}

export default AddLogins;
