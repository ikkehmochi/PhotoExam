import tensorflow as tf
import transformers
import numpy as np
import pandas as pd

MAXLEN = 256  # Maximum length of input sentence to the model.
BATCH_SIZE = 48

train_df = pd.read_json("id_snli-train.jsonl",lines=True)
valid_df = pd.read_json("id_snlidev.jsonl",lines=True)
test_df = pd.read_json("id_snli-test.jsonl",lines=True)

train_df["label"] = train_df["label"].apply(
    lambda x: 0 if x == "contradiction" else 1 if x == "entailment" else 2
)
y_train = tf.keras.utils.to_categorical(train_df.label, num_classes=3)

valid_df["label"] = valid_df["label"].apply(
    lambda x: 0 if x == "contradiction" else 1 if x == "entailment" else 2
)
y_val = tf.keras.utils.to_categorical(valid_df.label, num_classes=3)

test_df["label"] = test_df["label"].apply(
    lambda x: 0 if x == "contradiction" else 1 if x == "entailment" else 2
)
y_test = tf.keras.utils.to_categorical(test_df.label, num_classes=3)

class BertSemanticDataGenerator(tf.keras.utils.Sequence):
    """Generates batches of data.

    Args:
        sentence_pairs: Array of premise and hypothesis input sentences.
        labels: Array of labels.
        batch_size: Integer batch size.
        shuffle: boolean, whether to shuffle the data.
        include_targets: boolean, whether to incude the labels.

    Returns:
        Tuples `([input_ids, attention_mask, `token_type_ids], labels)`
        (or just `[input_ids, attention_mask, `token_type_ids]`
         if `include_targets=False`)
    """

    def __init__(
        self,
        sentence_pairs,
        labels,
        batch_size=BATCH_SIZE,
        shuffle=True,
        include_targets=True,
    ):
        self.sentence_pairs = sentence_pairs
        self.labels = labels
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.include_targets = include_targets
        # Load our BERT Tokenizer to encode the text.
        # We will use base-base-uncased pretrained model.
        self.tokenizer = transformers.BertTokenizer.from_pretrained(
            "indolem/indobert-base-uncased", do_lower_case=True
        )
        self.indexes = np.arange(len(self.sentence_pairs))
        self.on_epoch_end()

    def __len__(self):
        # Denotes the number of batches per epoch.
        return len(self.sentence_pairs) // self.batch_size

    def __getitem__(self, idx):
        # Retrieves the batch of index.
        indexes = self.indexes[idx * self.batch_size : (idx + 1) * self.batch_size]
        sentence_pairs = self.sentence_pairs[indexes]

        # With BERT tokenizer's batch_encode_plus batch of both the sentences are
        # encoded together and separated by [SEP] token.
        encoded = self.tokenizer.batch_encode_plus(
            sentence_pairs.tolist(),
            add_special_tokens=True,
            max_length=MAXLEN,
            return_attention_mask=True,
            return_token_type_ids=True,
            pad_to_max_length=True,
            return_tensors="tf",
        )

        # Convert batch of encoded features to numpy array.
        input_ids = np.array(encoded["input_ids"], dtype="int32")
        attention_masks = np.array(encoded["attention_mask"], dtype="int32")
        token_type_ids = np.array(encoded["token_type_ids"], dtype="int32")

        # Set to true if data generator is used for training/validation.
        if self.include_targets:
            labels = np.array(self.labels[indexes], dtype="int32")
            return [input_ids, attention_masks, token_type_ids], labels
        else:
            return [input_ids, attention_masks, token_type_ids]

    def on_epoch_end(self):
        # Shuffle indexes after each epoch if shuffle is set to True.
        if self.shuffle:
            np.random.RandomState(42).shuffle(self.indexes)

def check_similarity(sentence1, sentence2):
    model=tf.keras.models.load_model('firstiter.h5', custom_objects={"TFBertModel": transformers.TFBertModel})
    sentence_pairs = np.array([[str(sentence1), str(sentence2)]])
    test_data = BertSemanticDataGenerator(
        sentence_pairs, labels=None, batch_size=1, shuffle=False, include_targets=False,
    )
    labels=["contradiction", "entailment", "neutral"]
    proba = model.predict(test_data[0])[0]
    idx = np.argmax(proba)
    pred = labels[idx]
    if pred=="entailment" and proba[idx]>0.70:
        return 1
    elif pred=="neutral" and proba[idx]>0.85:
        return 1
    else:
        return 0

if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    sentence_1="Badan Penyelidik Usaha Persiapan Kemerdekaan Indonesia (BPUPKI) adalah badan yang dibentuk pada tahun 1945 oleh pemerintah pendudukan Jepang di Indonesia selama masa Perang Dunia II. Badan ini bertugas untuk menyelidiki dan merancang rencana kemerdekaan Indonesia setelah Jepang menyerah kepada Sekutu. BPUPKI terdiri dari berbagai pemimpin politik, tokoh masyarakat, dan tokoh agama dari berbagai latar belakang etnis di Indonesia. Salah satu tugas utamanya adalah merumuskan dasar negara dan konstitusi yang akan membentuk dasar bagi negara Indonesia merdeka. Hasil utama dari rapat-rapat BPUPKI adalah pembentukan Pancasila sebagai dasar negara Indonesia dan penyusunan UUD 1945, yang hingga kini menjadi konstitusi Indonesia. Setelah merumuskan dasar negara dan konstitusi, BPUPKI kemudian berkembang menjadi Panitia Persiapan Kemerdekaan Indonesia (PPKI) yang mengambil peran lebih lanjut dalam proses kemerdekaan Indonesia hingga proklamasi kemerdekaan pada tanggal 17 Agustus 1945."
    sentence_2="Panitia Persiapan Kemerdekaan Indonesia (PPKI) adalah lembaga yang dibentuk pada bulan Agustus 1945 untuk mempersiapkan proklamasi kemerdekaan Indonesia. PPKI terbentuk setelah Badan Penyelidik Usaha Persiapan Kemerdekaan Indonesia (BPUPKI) mengadakan sidangnya yang terakhir pada 18 Agustus 1945.PPKI terdiri dari tokoh-tokoh nasional Indonesia, termasuk pemimpin politik, tokoh agama, dan tokoh masyarakat dari berbagai daerah di Indonesia. Tugas utama PPKI adalah mengesahkan naskah proklamasi kemerdekaan Indonesia yang telah disiapkan oleh Soekarno dan Mohammad Hatta. Pada 17 Agustus 1945, PPKI secara resmi mengesahkan naskah proklamasi dan memutuskan untuk menyatakan kemerdekaan Indonesia.Selain itu, PPKI juga mengambil peran penting dalam menetapkan konstitusi sementara dan membentuk pemerintahan awal Indonesia. PPKI berperan dalam menjalankan proses awal negara Indonesia pasca-proklamasi kemerdekaan, menegaskan kedaulatan Indonesia, serta membentuk landasan politik dan administratif bagi negara yang baru merdeka."
    result =check_similarity(sentence1=sentence_1, sentence2=sentence_2)
    print(result)
